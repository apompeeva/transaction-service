from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from app.core.user_storage import UserStorage


class TransactionType(Enum):
    """Типы транзакций."""

    withdrawal = 1
    deposit = 2


@dataclass
class Transaction:
    """Данные транзакции."""

    user_id: int
    transaction_sum: Decimal
    transaction_type: TransactionType
    creation_time: datetime = field(default_factory=lambda: datetime.now())


class TransactionService:
    """Cервис обработки транзакций пользователя."""

    transactions: dict = {}
    reports: list = []
    users = UserStorage()

    @classmethod
    def calculate_balance_after_transaction(cls, transaction: Transaction) -> Decimal:
        """Рассчитать баланс после транзакции."""
        user = cls.users.get_user(transaction.user_id)
        balance = user.balance
        match transaction.transaction_type:
            case TransactionType.withdrawal:
                balance -= transaction.transaction_sum
            case TransactionType.deposit:
                balance += transaction.transaction_sum
        return balance

    @classmethod
    def put_transaction_in_storage(cls, transaction: Transaction):
        """Записать транзакцию в хранилище."""
        if transaction.user_id not in cls.transactions:
            cls.transactions[transaction.user_id] = []
        cls.transactions[transaction.user_id].append(transaction)

    @classmethod
    def update_balance(cls, user_id: int, new_balance: Decimal):
        """Обновить баланс."""
        user = cls.users.get_user(user_id)
        user.update_balance(new_balance)
        cls.users.update_user(user)

    @classmethod
    def create_transaction(
        cls, user_id: int, transaction_sum: Decimal, transaction_type: TransactionType,
    ) -> Transaction | None:
        """Создать транзакции."""
        transaction = Transaction(user_id, transaction_sum, transaction_type)
        new_balance = cls.calculate_balance_after_transaction(transaction)
        if new_balance > 0:
            cls.put_transaction_in_storage(transaction)
        else:
            if cls.users.get_user(user_id).is_verified():
                cls.put_transaction_in_storage(transaction)
            else:
                return None
        cls.update_balance(user_id, new_balance)
        return transaction

    @classmethod
    def get_transaction(
        cls, user_id: int, start_date: datetime, end_date: datetime,
    ) -> list[Transaction]:
        """Получить транзакцию."""
        if user_id not in cls.transactions:
            return []
        report = [
            transaction
            for transaction in cls.transactions[user_id]
            if start_date <= transaction.creation_time <= end_date
        ]
        cls.reports.append(report)
        return report
