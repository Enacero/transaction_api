from transaction_api.models.transaction import Transaction
from transaction_api.models.user import User
from transaction_api.services.database import db_service


def initialize_indexes():
    db_service.database.get_collection(User.collection_name).create_indexes(User.indexes)
    db_service.database.get_collection(Transaction.collection_name).create_indexes(Transaction.indexes)
