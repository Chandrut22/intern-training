import hashlib
import hmac
import time

from app.core.config import settings


def _current_time_window() -> int:
    return int(time.time() // settings.OTP_WINDOW_SECONDS)


def _dynamic_truncate(digest: bytes, digits: int) -> str:
    """RFC 4226 (HOTP) style dynamic truncation of an HMAC digest to an
    n-digit numeric code."""
    offset = digest[-1] & 0x0F

    binary_code = (
        (digest[offset] & 0x7F) << 24
        | (digest[offset + 1] & 0xFF) << 16
        | (digest[offset + 2] & 0xFF) << 8
        | (digest[offset + 3] & 0xFF)
    )

    return str(binary_code % (10**digits)).zfill(digits)


def _compute_otp(email: str, password_hash: str, time_window: int) -> str:
    message = f"{email}:{time_window}:{password_hash}".encode()
    secret = settings.OTP_SERVER_SECRET.encode()

    digest = hmac.new(secret, message, hashlib.sha256).digest()

    return _dynamic_truncate(digest, settings.OTP_DIGITS)


def generate_otp(email: str, password_hash: str) -> str:
    """Deterministically derive the current OTP for a user.

    Nothing is stored: the same code can be recomputed by
    `verify_otp` from the email, the window, and the user's current
    password hash. Once the password is reset, `password_hash`
    changes and every previously issued OTP stops verifying.
    """
    return _compute_otp(email, password_hash, _current_time_window())


def verify_otp(email: str, submitted_otp: str, password_hash: str) -> bool:
    """Verify a submitted OTP against the current and previous time
    windows (a grace period for submissions near a window boundary),
    using constant-time comparison."""
    if not submitted_otp or len(submitted_otp) != settings.OTP_DIGITS:
        return False

    current_window = _current_time_window()

    is_valid = False

    for window in (current_window, current_window - 1):
        expected = _compute_otp(email, password_hash, window)

        # Iterate over both windows unconditionally (no early return)
        # so verification time doesn't leak which window, if any,
        # matched.
        if hmac.compare_digest(expected, submitted_otp):
            is_valid = True

    return is_valid
