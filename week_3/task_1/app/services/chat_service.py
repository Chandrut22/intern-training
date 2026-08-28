import json
import logging
from collections.abc import AsyncIterable

import httpx
from app.core.settings import settings
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

logger = logging.getLogger(__name__)

_FALLBACK_STATUS_CODES = {401, 402, 403, 404, 429}


class ChatService:
    def __init__(self):
        self.url = str(settings.OPENROUTER_BASE_URL)
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

    @retry(
        # 1. Only retry on network errors or HTTP status errors (like 429, 502, 503, 504)
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        # 2. Wait exponentially: 2s, 4s, 8s, up to a maximum cap of 10s between retries
        wait=wait_exponential_jitter(initial=2, max=10, jitter=1),
        # 3. Stop trying after 5 total failed attempts
        stop=stop_after_attempt(5),
        # 4. If all 5 attempts fail, raise the original exception so the router can catch it
        reraise=True,
        # 5. Optional: Run a function to log the issue right before going to sleep
        before_sleep=lambda retry_state: logger.warning(
            f"API request failed. Retrying in {retry_state.next_action.sleep} seconds..."
        ),
    )
    async def _post_once(self, payload: dict) -> httpx.Response:
        """Single POST against OpenRouter. Retried by tenacity on transient errors."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response

    async def get_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = settings.TEMPERATURE,
        max_token: int = settings.MAX_TOKEN,
    ) -> dict:
        """Non-streaming chat completion with model fallback.

        Tries each model in ``models`` (defaults to ``settings.MODELS_NAME``)
        in order. On a fallback-eligible HTTP error, moves to the next model.
        Raises the last error if all models fail.
        """
        model_list = list(settings.MODELS_NAME)
        if not model_list:
            raise ValueError("No models configured — set MODELS_NAME in .env")

        print(model_list)

        payload = {
            "models": model_list,
            "messages": messages,
            "temperature": temperature,
            "max_completion_tokens": max_token,
        }
        try:
            response = await self._post_once(payload)
            logger.info("Chat completion succeeded with model")
            return response.json()

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status not in _FALLBACK_STATUS_CODES:
                raise

        except httpx.RequestError as exc:
            logger.error(f"Network error calling OpenRouter: {exc}")
            raise

    async def stream_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = settings.TEMPERATURE,
        max_token: int = settings.MAX_TOKEN,
    ) -> AsyncIterable[str]:

        model_list = list(settings.MODELS_NAME)

        if not model_list:
            raise ValueError("No models configured — set MODELS_NAME in .env")

        payload = {
            "models": model_list,
            "messages": messages,
            "temperature": temperature,
            "max_completion_tokens": max_token,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    self.url,
                    headers=self.headers,
                    json=payload,
                ) as response:
                    response.raise_for_status()

                    logger.info(f"Streaming from models: {model_list}")

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue

                        data = line[len("data:") :].strip()

                        if data == "[DONE]":
                            return

                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError:
                            logger.warning(f"Skipping malformed SSE chunk: {data!r}")
                            continue

                        delta = (
                            chunk.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content")
                        )

                        if delta:
                            yield delta

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code

            logger.warning(f"OpenRouter failed with HTTP {status}")

            if status not in _FALLBACK_STATUS_CODES:
                raise

            raise

        except httpx.RequestError as exc:
            logger.error(f"Network error opening stream: {exc}")
            raise
