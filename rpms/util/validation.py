"""
Validation utilities for the RPMS application.
"""
import re


def is_valid_email(email: str) -> bool:
    """Return True if email matches a standard email pattern."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def is_valid_mobile(mobile: str) -> bool:
    """Return True if mobile is exactly 10 digits."""
    if not mobile or not isinstance(mobile, str):
        return False
    return bool(re.match(r'^\d{10}$', mobile.strip()))


def is_valid_percentage(percentage) -> bool:
    """Return True if percentage is between 0 and 100 inclusive."""
    try:
        pct = float(percentage)
        return 0.0 <= pct <= 100.0
    except (TypeError, ValueError):
        return False


def is_valid_backlog_count(count) -> bool:
    """Return True if backlog count is a non-negative integer."""
    try:
        cnt = int(count)
        return cnt >= 0
    except (TypeError, ValueError):
        return False
