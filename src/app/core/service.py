from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum

import pytz

from app.core.user_storage import UserStorage
from app.crud.transactions_crud import (
    create_new_transaction,
    get_transaction_for_period,
    get_user_by_id,
    update_user_balance
)


class TransactionType(Enum):
    """Типы транзакций."""

    withdrawal = 'withdrawal'
    deposit = 'deposit'


@dataclass
class Transaction:
    """Данные транзакции."""

    user_id: int
    transaction_sum: int
    transaction_type: TransactionType
    creation_time: datetime = field(default_factory=lambda: datetime.now(UTC))

    def dict(self):
        """Возвращает словарь."""
        return asdict(self)


class TransactionService:
    """Cервис обработки транзакций пользователя."""

    transactions: dict = {}
    reports: list = []
    users = UserStorage()

    @classmethod
    async def calculate_balance_after_transaction(cls, transaction: Transaction) -> int:
        """Рассчитать баланс после транзакции."""
        user = await get_user_by_id(transaction.user_id)
        balance = user.balance
        match transaction.transaction_type:
            case TransactionType.withdrawal.value:
                balance -= transaction.transaction_sum
            case TransactionType.deposit.value:
                balance += transaction.transaction_sum
        return balance

    @classmethod
    async def put_transaction_in_storage(cls, transaction: Transaction):
        """Записать транзакцию в хранилище."""
        await create_new_transaction(transaction.dict())

    @classmethod
    async def update_balance(cls, user_id: int, new_balance: int):
        """Обновить баланс."""
        await update_user_balance(user_id, new_balance)

    @classmethod
    async def check_user_verified(cls, user_id: int) -> bool:
        """Проверить верификацию пользователя."""
        user = await get_user_by_id(user_id)
        return user.is_verified

    @classmethod
    async def create_transaction(
        cls, user_id: int, transaction_sum: int, transaction_type: TransactionType,
    ) -> Transaction | None:   # type: ignore
        """Создать транзакции."""
        transaction = Transaction(
            user_id, transaction_sum, transaction_type.value,  # type: ignore
        )
        new_balance = await cls.calculate_balance_after_transaction(transaction)
        if new_balance >= 0:
            await cls.put_transaction_in_storage(transaction)
        else:
            if await cls.check_user_verified(user_id):
                await cls.put_transaction_in_storage(transaction)
            else:
                return None
        await cls.update_balance(user_id, new_balance)
        return transaction

    @classmethod
    async def get_transaction(
        cls, user_id: int, start_date: datetime, end_date: datetime,
    ) -> list[Transaction]:
        """Получить транзакцию."""
        report = await get_transaction_for_period(
            user_id,
            start_date.astimezone(pytz.UTC),
            end_date.astimezone(pytz.UTC),
        )
        cls.reports.append(report)
        return report
