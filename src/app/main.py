from fastapi import FastAPI
from app.endpoints.endpoints import transaction_router


app = FastAPI()

app.include_router(transaction_router, tags=["transaction"])
