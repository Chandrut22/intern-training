import json
import os
from typing import Any
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

# Load environment variables from .env file
load_dotenv()



class Message(BaseModel):
    sender: str
    content: str
    timestamp: str | None = None


class Medication(BaseModel):
    name: str
    dose: str | None = None
    frequency: str | None = None



def get_api_key() -> str | None:
    return os.getenv("API_KEY")


def parse_message_json(json_str: str) -> Message | None:

    try:
        return Message.model_validate_json(json_str)
    except ValidationError as e:
        print(f"[ERROR] Failed to parse Message:\n{e}")
        return None


def parse_medications_file(file_path: str) -> list[Medication]:

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data: list[dict[str, Any]] = json.load(f)

    return [Medication.model_validate(item) for item in raw_data]




print("--- 1. Testing API Key Environment Variable ---")
api_key: str | None = get_api_key()
if api_key:
    print(f"Loaded API Key successfully: {api_key[:7]}***\n")
else:
    print("Warning: API_KEY not found in environment.\n")

print("--- 2. Validating Correct Records into Pydantic Models ---")
valid_med_json = '{"name": "Ibuprofen", "dose": "200mg", "frequency": "Every 6 hours"}'
valid_med: Medication = Medication.model_validate_json(valid_med_json)
print(f"Parsed Medication Model: {valid_med}")

optional_dose_med = Medication(name="Aspirin")
print(f"Medication without dose: {optional_dose_med}\n")

print("--- 3. Feeding Invalid Type Record & Catching Validation Error ---")
invalid_json_record = json.dumps(
        {
            "name": "Amoxicillin",
            "dose": {"amount": 500, "unit": "mg"},  # Wrong type!
        }
    )

try:
    print("Attempting to parse invalid JSON record...")
    Medication.model_validate_json(invalid_json_record)
except ValidationError as err:
    print("\nCaptured expected Pydantic ValidationError:")
    print(err)
