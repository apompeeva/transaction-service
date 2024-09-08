from fastapi import APIRouter, HTTPException, status
from opentracing import global_tracer

from app.core.service import TransactionService
from app.schemas.schemas import ReportData, Transaction

transaction_router = APIRouter()


@transaction_router.post('/create_transaction', status_code=status.HTTP_200_OK)
async def create_transaction(transaction: Transaction):
    """Создание транзакции."""
    with global_tracer().start_active_span('create_transaction') as scope:
        transaction_result = await TransactionService.create_transaction(
            transaction.user_id,
            transaction.transaction_sum,
            transaction.transaction_type,
        )
        if transaction_result is None:
            scope.span.set_tag('error', 'User not verified')
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User not verified',
            )


@transaction_router.post('/get_report', status_code=status.HTTP_200_OK)
async def get_report(report_data: ReportData):
    """Получение отчета о транзакциях за период."""
    with global_tracer().start_active_span('get_report') as scope:
        scope.span.set_tag('user_id', report_data.user_id)
        return await TransactionService.get_transaction(
            report_data.user_id,
            report_data.start_date,
            report_data.end_date,
        )


@transaction_router.get('/healthz/ready', status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка работоспособности сервиса."""
    return 'Ok'
