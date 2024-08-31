from fastapi import APIRouter, HTTPException, status

from app.core.service import TransactionService
from app.schemas.schemas import ReportData, Transaction

transaction_router = APIRouter()


@transaction_router.post("/create_transaction", status_code=status.HTTP_200_OK)
async def create_transaction(transaction: Transaction):
    """Создание транзакции."""
    transaction_result = await TransactionService.create_transaction(
        transaction.user_id,
        transaction.transaction_sum,
        transaction.transaction_type,
    )
    if transaction_result is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not verified",
        )


@transaction_router.post("/get_report", status_code=status.HTTP_200_OK)
async def get_report(report_data: ReportData):
    """Получение отчета о транзакциях за период."""
    return await TransactionService.get_transaction(
        report_data.user_id,
        report_data.start_date,
        report_data.end_date,
    )


@transaction_router.get("/healthz/ready", status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка работоспособности сервиса."""
    return "Ok"
