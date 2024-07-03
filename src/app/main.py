import datetime
from dataclasses import dataclass
from enum import Enum


class TransactionType(Enum):
    """Типы транзакций."""

    write_off = 1
    replenishment = 2


@dataclass
class Transaction:
    """Данные транзакции."""

    user_id: int
    transaction_sum: float
    transaction_type: TransactionType
    creation_time: datetime.datetime = datetime.datetime.now()


class TransactionService:
    """Cервис обработки транзакций пользователя."""

    transactions: dict = {}
    reports: list = []

    @classmethod
    def create_transaction(cls, user_id, transaction_sum, transaction_type):
        """Создать транзакции."""
        transaction = Transaction(user_id, transaction_sum, transaction_type)

        if user_id not in cls.transactions:
            cls.transactions[user_id] = []
        cls.transactions[user_id].append(transaction)
        return transaction

    @classmethod
    def get_transaction(cls, user_id, start_date, end_date):
        """Получить тарнзакцию."""
        if user_id not in cls.transactions:
            return []
        report = [
            transaction
            for transaction in cls.transactions[user_id]
            if start_date <= transaction.creation_time <= end_date
        ]
        cls.reports.append(report)
        return report
