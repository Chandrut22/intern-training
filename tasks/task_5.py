

from __future__ import annotations

import json
import logging
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from src.role import Role
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class TranscriptError(Exception):
    """Raised when a transcript is structurally invalid in a domain-specific way."""


@dataclass
class Message:
    """One transcript message, decorated with a per-record request ID."""
    role: Role
    content: str
    tokens: int
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOOD_PATH = PROJECT_ROOT / "tasks" / "data" / "transcript.json"
BAD_PATH = PROJECT_ROOT / "tasks" / "data" / "transcript_broken.json"


def load_transcript(path: Path) -> list[dict[str, Any]]:
    """Load a transcript JSON file. Returns [] on missing or malformed input.

    Raises:
        FileNotFoundError: propgated so the caller can decide.
        TranscriptError:   if every message is structurally invalid.
    """
    if not path.exists():
        logger.warning("Transcript file not found: %s", path)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        logger.warning(
            "Malformed JSON in %s at line %d column %d: %s",
            path, exc.lineno, exc.colno, exc.msg,
        )
        return []

    if not isinstance(data, list):
        logger.warning("Expected a JSON array in %s, got %s", path, type(data).__name__)
        return []

    return data


def parse_messages(raw: list[dict[str, Any]]) -> list[Message]:
    """Parse raw dicts into Message objects. Skips entries with bad roles."""
    out: list[Message] = []
    for entry in raw:
        try:
            role = Role(entry["role"])
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping entry with invalid role %r: %s", entry.get("role"), exc)
            continue
        out.append(
            Message(
                role=role,
                content=entry.get("content", ""),
                tokens=int(entry.get("tokens", 0)),
            )
        )

    if not out:
        raise TranscriptError(f"No valid messages found in transcript ({len(raw)} entries).")
    return out


def utc_now() -> datetime:
    """Current time as timezone-aware UTC."""
    return datetime.now(timezone.utc)



def report_totals(messages: list[Message]) -> dict[str, dict[str, int]]:
    """Return {role_value: {"count": N, "tokens": T}} using Counter + defaultdict."""
    counts: Counter[str] = Counter()
    tokens: defaultdict[str, int] = defaultdict(int)
    for m in messages:
        counts[m.role.value] += 1
        tokens[m.role.value] += m.tokens
    return {role: {"count": counts[role], "tokens": tokens[role]} for role in counts}


def _run(path: Path) -> None:
    now = utc_now()
    logger.warning("Loading transcript at %s @ %s", utc_now().isoformat(), path.name)

    raw = load_transcript(path)
    if not raw:
        logger.warning("No messages loaded from %s; exiting cleanly.", path)
        return

    try:
        messages = parse_messages(raw)
    except TranscriptError as exc:
        logger.warning("%s", exc)
        return

    start = time.perf_counter()
    totals = report_totals(messages)
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(f"loaded_at_utc   : {now.isoformat()}")
    print(f"message_count   : {len(messages)}")
    print(f"first_request_id: {messages[0].request_id}")
    print(f"totals_per_role : {totals}")
    print(f"report_time_ms  : {elapsed_ms:.3f}")


def _ensure_sample_files() -> None:
    """Create a valid + a malformed JSON file under tasks/data/ for the demo."""
    data_dir = PROJECT_ROOT / "tasks" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    good = data_dir / "transcript.json"
    if not good.exists():
        good.write_text(
            json.dumps(
                [
                    {"role": "system",    "content": "You are a helpful assistant.", "tokens": 6},
                    {"role": "user",      "content": "Hello!",                        "tokens": 2},
                    {"role": "assistant", "content": "Hi! How can I help?",           "tokens": 6},
                    {"role": "user",      "content": "Explain dicts.",                "tokens": 3},
                    {"role": "assistant", "content": "Key-value pairs.",              "tokens": 3},
                ],
                indent=2,
            ),
            encoding="utf-8",
        )

    bad = data_dir / "transcript_broken.json"
    if not bad.exists():
        bad.write_text(
            '[\n  {"role": "user", "content": "hi", "tokens": 1}\n',
            encoding="utf-8",
        )


if __name__ == "__main__":
    _ensure_sample_files()

    print("── good transcript ──")
    _run(GOOD_PATH)

    print("\n── malformed transcript (missing '}') ──")
    _run(BAD_PATH)
