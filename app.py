from fastapi import FastAPI

from transaction_api.api.statistics import router as statistics_router
from transaction_api.api.transactions import router as transactions_router
from transaction_api.api.users import router as user_router
from transaction_api import initialize


def create_app(*args, **kwargs):
    initialize.initialize_indexes()
    app = FastAPI()

    app.include_router(user_router)
    app.include_router(statistics_router)
    app.include_router(transactions_router)
    return app
