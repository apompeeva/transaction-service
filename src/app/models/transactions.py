import datetime
import enum
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, MetaData, Table, text
from sqlalchemy.orm import Mapped, mapped_column, registry

from app.database import Base, sync_engine

metadata = MetaData()


class TransactionType(enum.Enum):
    """Типы транзакций."""

    deposit = 'deposit'
    withdrawal = 'withdrawal'


class TransactionModel(Base):
    """Модель для таблицы transactions."""

    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'transaction_schema'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('auth_schema.users.id'))
    transaction_type: Mapped[TransactionType]
    transaction_sum: Mapped[int] = mapped_column(BigInteger, nullable=False)
    creation_time: Mapped[Annotated[datetime.datetime, mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())"),
    )]]


mapper_registry = registry()

users_table = Table(
    'users', Base.metadata, autoload_with=sync_engine, schema='auth_schema',
)


class Users:
    """Класс для маппинга таблицы users."""

    pass


mapper_registry.map_imperatively(Users, users_table)
