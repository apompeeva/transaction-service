import datetime

from sqlalchemy import and_, select

from app.database import async_session_maker
from app.models.transactions import TransactionModel, Users


async def create_new_transaction(transaction_dict: dict):
    """Добавление записи в таблицу transactions."""
    async with async_session_maker() as session:
        db_transaction = TransactionModel(**transaction_dict)
        session.add(db_transaction)
        await session.commit()


async def get_transaction_for_period(
    user_id: int,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """Получение транзакций пользователя за период времени."""
    async with async_session_maker() as session:
        query = select(TransactionModel).where(
            and_(
                TransactionModel.user_id == user_id,
                TransactionModel.creation_time >= start_date,
                TransactionModel.creation_time <= end_date,
            ),
        )
        report = await session.execute(query)
        return report.scalars().all()


async def update_user_balance(user_id: int, new_balance: int):
    """Обновление баланса пользователя."""
    async with async_session_maker() as session:
        user = await session.get(Users, user_id)
        user.balance = new_balance
        await session.commit()


async def get_user_by_id(user_id: int):
    """Получение пользователя по id."""
    async with async_session_maker() as session:
        query = select(Users).where(Users.id == user_id)
        user = await session.execute(query)
        return user.scalars().first()
