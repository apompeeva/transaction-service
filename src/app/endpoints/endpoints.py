from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.schemas import Transaction, ReportData
from app.core.service import TransactionService

transaction_router = APIRouter()


@transaction_router.post("/create_transaction", status_code=status.HTTP_200_OK)
async def create_transaction(transaction: Transaction):
    result = TransactionService.create_transaction(
        transaction.user_id, transaction.transaction_sum, transaction.transaction_type)
    if result is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not verified")


@transaction_router.post("/get_report", status_code=status.HTTP_200_OK)
async def get_report(data: ReportData):
    report = TransactionService.get_transaction(
        data.user_id, data.start_date, data.end_date)
    return report
