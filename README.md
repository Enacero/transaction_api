# Transaction Management System

## Overview
This project is a **Transaction Management System** designed to manage users and their transactions. It features robust RESTful APIs implemented using **FastAPI**, dependency management with **Poetry**, and a **MongoDB** database. The project is containerized with **Docker** and orchestrated using **Docker Compose** for seamless deployment.

---

## Technologies Used
- **FastAPI**: For building the RESTful APIs.
- **Poetry**: For dependency management and packaging.
- **MongoDB**: As the database for storing user and transaction data.
- **Docker**: For containerizing the application.
- **Docker Compose**: To manage multi-container setups for the application and database.
- **Python 3.12**: As the programming language.

---

## Features
### User Management
- Create, retrieve, and delete users.
- Enforce unique user IDs and validate email formats.

### Transaction Management
- Add and retrieve transactions for users.
- Prevent negative balances with server-side validation.
- Retrieve account summaries dynamically (e.g., balance and transaction count).

---

## Setup Instructions

### Prerequisites
- **Docker** and **Docker Compose** installed.
- **Python 3.12** and **Poetry** (optional, for local setup).

### Running the Application with Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/Enacero/transaction_api.git
   cd transaction_api
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. The API server will be available at `http://localhost:8000`.

4. Access the automatically generated API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Local Development Setup (Optional)
1. Clone the repository:
   ```bash
   git clone https://github.com/Enacero/transaction_api.git
   cd transaction_api
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Start the MongoDB instance using Docker:
   ```bash
   docker-compose up mongodb
   ```

4. Run the application locally:
   ```bash
   poetry run uvicorn app:app --reload
   ```

5. Set the `MONGO_DB_HOST` environment variable to specify the MongoDB host:
   ```bash
   export MONGO_DB_HOST=localhost
   ```

---

## Populating the Database with Test Data

To prepopulate the database with test data:
1. Ensure the application and MongoDB are running:
   ```bash
   docker-compose up
   ```

2. Use the `populate_data` service defined in `docker-compose.yml` to insert sample users and transactions:
   ```bash
   docker-compose run populate_data
   ```

This will load sample user and transaction data into the database for testing purposes.

---

## API Endpoints

### User Management
#### Get All Users
**GET /users**
```bash
curl -X 'GET' \
  'http://localhost:8000/users' \
  -H 'accept: application/json'
```
Response:
```json
[
  {
    "userId": "user1",
    "name": "Alice Smith",
    "email": "alice@example.com",
    "createdAt": "2024-12-14T19:03:09.027930"
  }
]
```

#### Add a User
**POST /users**
```bash
curl -X 'POST' \
  'http://localhost:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "userId": "user1",
  "name": "Alice Smith",
  "email": "alice@example.com"
}'
```
Response:
```json
{
  "success": true,
  "message": "User created successfully."
}
```

#### Get a User
**GET /users/{userId}**
```bash
curl -X 'GET' \
  'http://localhost:8000/users/user1' \
  -H 'accept: application/json'
```
Response:
```json
{
  "userId": "user1",
  "name": "Alice Smith",
  "email": "alice@example.com",
  "createdAt": "2024-12-14T19:03:09.027930"
}
```

#### Delete a User
**DELETE /users/{userId}**
```bash
curl -X 'DELETE' \
  'http://localhost:8000/users/user1' \
  -H 'accept: application/json'
```
Response:
```json
{
  "success": true,
  "message": "User deleted successfully."
}
```

### Transaction Management
#### Add a Transaction
**POST /transactions**
```bash
curl -X 'POST' \
  'http://localhost:8000/transactions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "transactionId": "trxn123",
  "userId": "user1",
  "amount": 100.5,
  "timestamp": "2024-12-14T19:03:09.027930"
}'
```
Response:
```json
{
  "success": true,
  "message": "Transaction created successfully."
}
```

#### List Transactions
**GET /transactions**
```bash
curl -X 'GET' \
  'http://localhost:8000/transactions?userId=user1' \
  -H 'accept: application/json'
```
Response:
```json
[
  {
    "transactionId": "trxn123",
    "userId": "user1",
    "amount": 100.5,
    "timestamp": "2024-12-14T19:03:09.027930"
  }
]
```

#### Account Summary
**GET /account-summary/{userId}**
```bash
curl -X 'GET' \
  'http://localhost:8000/account-summary/user1' \
  -H 'accept: application/json'
```
Response:
```json
{
  "userId": "user1",
  "currentBalance": 100.5,
  "transactionCount": 1
}
```

---

## Testing

### Run Tests
To execute unit tests:
```bash
tox -e 3.12
```
