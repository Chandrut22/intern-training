

from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
import json
import logging
from pathlib import Path
import re
import time
from typing import Any
import uuid

from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


PHONE_REGEX = re.compile(
    r"(?<!\d)(?:\(?\d{3}\)?[\s\-\.]*)\d{3}[\s\-\.]*\d{4}(?!\d)"
)

PRICING_PER_1K: dict[str, dict[str, Decimal]] = {
    "system": {"input": Decimal("0.0025"), "output": Decimal("0.0000")},
    "user": {"input": Decimal("0.0025"), "output": Decimal("0.0000")},
    "assistant": {"input": Decimal("0.0000"), "output": Decimal("0.0100")},
}


class MessageInput(BaseModel):
    """Raw incoming message schema for validation."""

    role: str
    content: str
    tokens: int = Field(ge=0)


class ProcessedMessage(BaseModel):
    """Validated, processed message schema with system metadata."""

    id: uuid.UUID
    role: str
    content: str
    tokens: int
    cost: Decimal
    processed_at_utc: datetime


def redact_phone_numbers(text: str) -> str:
    """Replaces 10-digit phone numbers in a block of text with [PHONE]."""
    return PHONE_REGEX.sub("[PHONE]", text)


def compute_cost(role: str, tokens: int) -> Decimal:
    """Calculates exact token cost using Decimal arithmetic."""
    rates = PRICING_PER_1K.get(
        role.lower(), {"input": Decimal("0.0025"), "output": Decimal("0.0100")}
    )
    rate_per_1k = rates["output"] if role.lower() == "assistant" else rates["input"]
    return (Decimal(tokens) / Decimal(1000)) * rate_per_1k


def process_message_record(raw_record: dict[str, Any]) -> ProcessedMessage | None:
    """Validates and transforms a single raw message dict into a ProcessedMessage.

    Returns None if validation fails.
    """
    try:
        validated = MessageInput.model_validate(raw_record)
    except ValidationError as err:
        logger.warning("Skipping invalid record: %s", err.errors()[0]["msg"])
        return None

    redacted_content = redact_phone_numbers(validated.content)
    cost = compute_cost(validated.role, validated.tokens)

    return ProcessedMessage(
        id=uuid.uuid4(),
        role=validated.role.lower(),
        content=redacted_content,
        tokens=validated.tokens,
        cost=cost,
        processed_at_utc=datetime.now(timezone.utc),
    )


def process_pipeline(file_path: Path) -> dict[str, Any]:
    """Reads a JSON file, processes valid records, skips invalid ones, and reports totals."""
    start_time = time.perf_counter()

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found at: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as err:
            logger.error("Failed to parse JSON file: %s", err)
            return {"status": "error", "message": str(err)}

    processed_records: list[ProcessedMessage] = []
    skipped_count = 0

    tokens_per_role: dict[str, int] = defaultdict(int)
    cost_per_role: dict[str, Decimal] = defaultdict(Decimal)

    for item in raw_data:
        record = process_message_record(item)
        if record is None:
            skipped_count += 1
            continue

        processed_records.append(record)
        tokens_per_role[record.role] += record.tokens
        cost_per_role[record.role] += record.cost

    execution_time = time.perf_counter() - start_time

    return {
        "status": "success",
        "processed_count": len(processed_records),
        "skipped_count": skipped_count,
        "tokens_per_role": dict(tokens_per_role),
        "cost_per_role": dict(cost_per_role),
        "execution_time_seconds": round(execution_time, 6),
        "records": processed_records,
    }



def test_phone_number_redaction():
    """Test 1: Ensures 10-digit phone numbers are redacted correctly."""
    raw = "Reach me at 123-456-7890 or 9876543210."
    assert redact_phone_numbers(raw) == "Reach me at [PHONE] or [PHONE]."


def test_decimal_cost_precision():
    """Test 2: Verifies exact Decimal cost calculation without float drift."""
    cost = compute_cost("user", 1000)
    assert cost == Decimal("0.0025")
    assert isinstance(cost, Decimal)


def test_valid_record_processing():
    """Test 3: Validates UUID assignment and phone redaction on valid input."""
    data = {"role": "user", "content": "Call 555-123-4567", "tokens": 500}
    record = process_message_record(data)
    assert record is not None
    assert record.role == "user"
    assert record.content == "Call [PHONE]"
    assert isinstance(record.id, uuid.UUID)


def test_invalid_record_skipping():
    """Test 4: Verifies invalid schema records return None and are safely skipped."""
    bad_data = {"role": "user", "content": "Missing tokens"}
    assert process_message_record(bad_data) is None

    negative_tokens = {"role": "user", "content": "Bad tokens", "tokens": -10}
    assert process_message_record(negative_tokens) is None


def test_pipeline_clean_file(tmp_path: Path):
    """Test 5: Tests end-to-end processing on a valid clean file."""
    clean_data = [
        {"role": "system", "content": "Initialize", "tokens": 100},
        {"role": "user", "content": "Hello 123-456-7890", "tokens": 200},
    ]
    file_path = tmp_path / "clean.json"
    file_path.write_text(json.dumps(clean_data), encoding="utf-8")

    result = process_pipeline(file_path)
    assert result["status"] == "success"
    assert result["processed_count"] == 2
    assert result["skipped_count"] == 0
    assert result["tokens_per_role"]["system"] == 100
    assert result["tokens_per_role"]["user"] == 200


def test_pipeline_broken_file(tmp_path: Path):
    """Test 6: Tests end-to-end processing skipping broken records."""
    mixed_data = [
        {"role": "user", "content": "Valid text", "tokens": 100},
        {"role": "assistant"},  # Missing content and tokens
        {"content": "No role", "tokens": 50},  # Missing role
    ]
    file_path = tmp_path / "broken.json"
    file_path.write_text(json.dumps(mixed_data), encoding="utf-8")

    result = process_pipeline(file_path)
    assert result["status"] == "success"
    assert result["processed_count"] == 1
    assert result["skipped_count"] == 2





print("--- Running Gate Pipeline Demonstration ---\n")

clean_file = Path("demo_clean_messages.json")
broken_file = Path("demo_broken_messages.json")

clean_sample = [
        {"role": "system", "content": "System operational.", "tokens": 150},
        {
            "role": "user",
            "content": "Call support at 800-555-0199 or 555-014-9988.",
            "tokens": 450,
        },
        {"role": "assistant", "content": "Understood. Account confirmed.", "tokens": 300},
    ]

broken_sample = [
        {"role": "user", "content": "Valid user record", "tokens": 200},
        {"role": "user", "content": "Broken record missing tokens"},
        {"role": "assistant", "content": "Negative tokens test", "tokens": -50},
        {
            "role": "assistant",
            "content": "Reach agent at 987-654-3210 for details.",
            "tokens": 500,
        },
    ]

clean_file.write_text(json.dumps(clean_sample, indent=2), encoding="utf-8")
broken_file.write_text(json.dumps(broken_sample, indent=2), encoding="utf-8")

    # Run clean file
print("1. Processing CLEAN input file:")
res_clean = process_pipeline(clean_file)
print(f"   - Processed: {res_clean['processed_count']}")
print(f"   - Skipped:   {res_clean['skipped_count']}")
print(f"   - Tokens:    {res_clean['tokens_per_role']}")
print(f"   - Costs:     {res_clean['cost_per_role']}")
print(f"   - Duration:  {res_clean['execution_time_seconds']}s\n")

    # Run broken file
print("2. Processing BROKEN input file:")
res_broken = process_pipeline(broken_file)
print(f"   - Processed: {res_broken['processed_count']}")
print(f"   - Skipped:   {res_broken['skipped_count']}")
print(f"   - Tokens:    {res_broken['tokens_per_role']}")
print(f"   - Costs:     {res_broken['cost_per_role']}")
print(f"   - Duration:  {res_broken['execution_time_seconds']}s\n")

clean_file.unlink(missing_ok=True)
broken_file.unlink(missing_ok=True)

print("Pipeline execution complete. To run the test suite:")
print(f"  uv run pytest {Path(__file__).name}")