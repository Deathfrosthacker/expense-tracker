import re
from datetime import datetime
from markupsafe import escape


VALID_CATEGORIES = [
    'food', 'transport', 'utilities', 'entertainment',
    'health', 'shopping', 'education', 'other'
]


def sanitize_input(text: str) -> str:
    if not text:
        return ""
    return escape(text)[:500]


def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0 or amount > 999999.99:
            return None
        return round(amount, 2)
    except (ValueError, TypeError):
        return None


def validate_category(category: str) -> bool:
    return category in VALID_CATEGORIES


def validate_date(date_str: str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date > datetime.now():
            return None
        return date_str
    except ValueError:
        return None