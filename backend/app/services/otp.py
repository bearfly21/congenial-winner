"""
OTP Service — Mock implementation for hackathon.
In production, replace with SMS provider (e.g., Twilio, Eskiz.uz).
"""

import random
from typing import Dict, Tuple

# In-memory OTP store: {phone_number: otp_code}
_otp_store: Dict[str, str] = {}


def send_otp(phone: str) -> str:
    """Generate and 'send' OTP. Returns the code (for mock/debug purposes)."""
    code = "1234"  # Fixed code for easy testing. In prod: str(random.randint(1000, 9999))
    _otp_store[phone] = code
    print(f"[OTP Mock] Code for {phone}: {code}")
    return code


def verify_otp(phone: str, code: str) -> bool:
    """Verify OTP code. Returns True if valid."""
    stored = _otp_store.get(phone)
    if stored is None:
        return False
    if stored == code:
        # Remove used OTP
        del _otp_store[phone]
        return True
    return False
