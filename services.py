from models import Expense
from utils import (
    validate_amount,
    validate_category,
    validate_date,
    sanitize_input
)


def add_expense(data):
    amount = validate_amount(data.get("amount"))
    if amount is None:
        return False, "Invalid amount"

    category = data.get("category", "").lower().strip()
    if not validate_category(category):
        return False, "Invalid category"

    description = sanitize_input(data.get("description", ""))
    date = validate_date(data.get("date"))

    if not date:
        return False, "Invalid date"

    Expense.create(amount, category, description, date)
    return True, "Expense added successfully"


def delete_expense(expense_id):
    Expense.delete(expense_id)
    return True, "Expense deleted successfully"