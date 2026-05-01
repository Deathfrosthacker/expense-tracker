from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import add_expense, delete_expense
from models import Expense
from utils import VALID_CATEGORIES

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    expenses = Expense.get_all()
    total = Expense.total_spending()
    categories = Expense.category_summary()

    return render_template(
        "index.html",
        expenses=expenses,
        total_spending=total,
        category_summary=categories,
        categories=VALID_CATEGORIES
    )


@bp.route("/add", methods=["POST"])
def add():
    success, message = add_expense(request.form)

    flash(message, "success" if success else "error")
    return redirect(url_for("main.index"))


@bp.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    delete_expense(expense_id)
    flash("Deleted successfully", "success")
    return redirect(url_for("main.index"))