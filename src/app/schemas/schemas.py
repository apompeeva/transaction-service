from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionType(Enum):
    """Типы транзакций."""

    withdrawal = 'withdrawal'
    deposit = 'deposit'


class Transaction(BaseModel):
    """Данные для создания транзакции."""

    user_id: int
    transaction_sum: float
    transaction_type: TransactionType


class TransactionGet(Transaction):
    """Данные для получения транзакции."""

    user_id: int
    transaction_sum: float
    transaction_type: TransactionType
    creation_time: datetime


class ReportData(BaseModel):
    """Данные для получения отчета о транзакциях за период."""

    user_id: int
    start_date: datetime
    end_date: datetime


class Report(BaseModel):
    """Модель для получения списка отчетов."""

    report: list[TransactionGet]
