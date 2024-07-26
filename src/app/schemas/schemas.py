from pydantic import BaseModel
from enum import IntEnum
from datetime import datetime


class TransactionType(IntEnum):
    withdrawal = 1
    deposit = 2


class Transaction(BaseModel):
    user_id: int
    transaction_sum: float
    transaction_type: TransactionType


class TransactionGet(Transaction):
    user_id: int
    transaction_sum: float
    transaction_type: TransactionType
    creation_time: datetime


class ReportData(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime


class Report(BaseModel):
    report: list[TransactionGet]
