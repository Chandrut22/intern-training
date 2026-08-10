import re


def extract_json_from_fences(text: str) -> str:

    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

PHONE_REGEX = re.compile(r"(?<!\d)(?:\d[\s\-\.]*){9}\d(?!\d)")

IDENTIFIER_REGEX = re.compile(r"^[A-Z]{3}-\d{4}$")


def redact_phone_numbers(text: str) -> str:
    return PHONE_REGEX.sub("[PHONE]", text)



def run_tests():
    print("--- Running Tests ---")

    print("\n1. Testing extract_json_from_fences:")

    fenced_text = '```json\n{"key": "value"}\n```'
    assert extract_json_from_fences(fenced_text) == '{"key": "value"}'

    plain_text = '{"key": "value"}'
    assert extract_json_from_fences(plain_text) == '{"key": "value"}'

    prose_text = 'Here is the response:\n```json\n{"status": "ok"}\n```\nHope that helps!'
    assert extract_json_from_fences(prose_text) == '{"status": "ok"}'

    non_latin_text = 'यह आपका डेटा है:\n```\n{"नाम": "अमित"}\n```'
    assert extract_json_from_fences(non_latin_text) == '{"नाम": "अमित"}'

    print("  [PASS] All fence stripping tests passed.")

    print("\n2. Testing Regexes:")

    assert IDENTIFIER_REGEX.match("ABC-1234") is not None
    assert IDENTIFIER_REGEX.match("abc-1234") is None 
    assert IDENTIFIER_REGEX.match("ABCD-1234") is None  
    assert IDENTIFIER_REGEX.match("ABC-123") is None  
    assert IDENTIFIER_REGEX.match("АБВ-1234") is None 
    assert IDENTIFIER_REGEX.match("ABC-12345") is None  

    print("  [PASS] Identifier regex validation tests passed.")


    print("\n3. Testing Phone Redaction:")

    t1 = "Call me at 1234567890 or 123-456-7890."
    assert redact_phone_numbers(t1) == "Call me at [PHONE] or [PHONE]."

    t2 = "Account ID: 12345678901 (11 digits)"
    assert redact_phone_numbers(t2) == "Account ID: 12345678901 (11 digits)"

    t3 = "कृपया मुझे 9876543210 पर कॉल करें या फिर 987-654-3210 पर संपर्क करें।"
    expected_t3 = "कृपया मुझे [PHONE] पर कॉल करें या फिर [PHONE] पर संपर्क करें।"
    assert redact_phone_numbers(t3) == expected_t3


    print("  [PASS] Phone number redaction tests passed.")
    print("\n--- All Tests Successfully Passed! ---")


if __name__ == "__main__":
    run_tests()