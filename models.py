import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID
import uuid
from db import get_db


DATABASE = "expenses.db"

class Expense:
    def __init__(
        self,
        id: Optional[int],
        amount: float,
        category: str,
        description: str,
        date: str,
        reference: str = str(uuid.uuid4()),
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.reference = reference
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
        self.created_at = created_at or datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "reference": self.reference,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "created_at": self.created_at,
        }

    @staticmethod
    def create(amount: float, category: str, description: str, date: str) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses (amount, category, description, date)
                VALUES (?, ?, ?, ?)
                """,
                (amount, category, description, date),
            )
            return cursor.lastrowid

    @staticmethod
    def delete(expense_id: int) -> None:
        with get_db() as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    @staticmethod
    def get_all() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                """
                SELECT id, amount, category, description, date, created_at
                FROM expenses
                ORDER BY date DESC, created_at DESC
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(expense_id: int) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM expenses WHERE id = ?",
                (expense_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def total_spending() -> float:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM expenses"
            )
            return cursor.fetchone()["total"]

    @staticmethod
    def category_summary() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                """
                SELECT category,
                       COALESCE(SUM(amount), 0) as total,
                       COUNT(*) as count
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def monthly_summary(limit: int = 6) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                """
                SELECT strftime('%Y-%m', date) as month,
                       COALESCE(SUM(amount), 0) as total
                FROM expenses
                GROUP BY month
                ORDER BY month DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]