from datetime import datetime
import random
import string

from transaction_api.models.transaction import Transaction
from transaction_api.models.user import User
from transaction_api.services.database import db_service


def generate_user_id():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


user_data = [
    {
        "user_id": "user1",
        "name": "Alice Smith",
        "email": "alice@example.com",
        "created_at": datetime.now().isoformat(),
        "balance": 100.0,
    },
    {
        "user_id": "user2",
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "created_at": datetime.now().isoformat(),
        "balance": 150.0,
    },
    {
        "user_id": "user3",
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "created_at": datetime.now().isoformat(),
        "balance": 200.0,
    },
]


def generate_transaction_data(user_id):
    return {
        "user_id": user_id,
        "transaction_id": "".join(random.choices(string.ascii_lowercase + string.digits, k=12)),
        "amount": random.uniform(5.0, 500.0),
        "timestamp": datetime.now().isoformat(),
    }


def insert_users():
    print("Inserting users...")
    users_collection = db_service.database.get_collection(User.collection_name)
    for user in user_data:
        if users_collection.find_one({"user_id": user["user_id"]}) is None:
            users_collection.insert_one(user)
            print(f"Inserted user: {user['user_id']}")


def insert_transactions():
    print("Inserting transactions...")
    for user in user_data:
        for _ in range(random.randint(1, 5)):
            transaction_data = generate_transaction_data(user["user_id"])
            db_service.database.get_collection(Transaction.collection_name).insert_one(transaction_data)
            print(f"Inserted transaction for {user['user_id']} with ID: {transaction_data['transaction_id']}")


def main():
    insert_users()
    insert_transactions()


if __name__ == "__main__":
    main()
