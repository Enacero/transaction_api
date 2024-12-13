# Transaction Management System

## Overview

The Transaction Management System is a RESTful API designed to handle user and transaction data with robust business logic, validation, and persistence in a MongoDB database. The application is built using FastAPI and packaged with Docker for easy deployment.

---

## Features

- User management: Create, retrieve, and delete users.
- Transaction management: Add, list, and filter transactions.
- Account summary: Retrieve user account details, including balance and transaction count.
- Validation: Ensures data integrity and business rules enforcement.
- Prepackaged with Docker Compose for streamlined deployment.

---

## Prerequisites

- Docker and Docker Compose installed on your system.
---

## Setup Instructions

### Clone Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### Build and Run with Docker Compose

1. Build the Docker images:

   ```bash
   docker-compose build
   ```

2. Start the containers:

   ```bash
   docker-compose up
   ```

   The application will be available at `http://localhost:8000`.

---

## API Documentation

The API documentation is available at `http://localhost:8000/docs`.

You can explore and test the endpoints interactively using Swagger UI.

---

## OpenAPI Specification

Here is the OpenAPI specification for this project, which describes all endpoints, request bodies, and responses:

### Key Endpoints

#### **User Management**

1. **Create User**

   - **Endpoint:** `POST /users`
   - **Request Body:**
     ```json
     {
       "userId": "string",
       "name": "string",
       "email": "string"
     }
     ```
   - **Response:**
     ```json
     {
       "success": true,
       "message": "User created successfully."
     }
     ```

2. **Get User**

   - **Endpoint:** `GET /users/{userId}`
   - **Response:**
     ```json
     {
       "userId": "string",
       "name": "string",
       "email": "string",
       "createdAt": "string (ISO format)"
     }
     ```

3. **Delete User**

   - **Endpoint:** `DELETE /users/{userId}`
   - **Response:**
     ```json
     {
       "success": true,
       "message": "User deleted successfully."
     }
     ```

#### **Transaction Management**

1. **Create Transaction**

   - **Endpoint:** `POST /transactions`
   - **Request Body:**
     ```json
     {
       "transactionId": "string",
       "userId": "string",
       "amount": "number",
       "timestamp": "string (ISO format)"
     }
     ```
   - **Response:**
     ```json
     {
       "success": true,
       "message": "Transaction created successfully."
     }
     ```

2. **List Transactions**

   - **Endpoint:** `GET /transactions`
   - **Query Parameters:**
     - `userId` (required)
     - `startDate` (optional)
     - `endDate` (optional)
   - **Response:**
     ```json
     [
       {
         "transactionId": "string",
         "userId": "string",
         "amount": "number",
         "timestamp": "string"
       }
     ]
     ```

#### **Account Summary**

1. **Get Account Summary**
   - **Endpoint:** `GET /account-summary/{userId}`
   - **Response:**
     ```json
     {
       "userId": "string",
       "currentBalance": "number",
       "transactionCount": "number"
     }
     ```

---

## Example cURL Commands

### Create a User

```bash
curl -X POST http://localhost:8000/users \
     -H "Content-Type: application/json" \
     -d '{"userId": "user1", "name": "Alice", "email": "alice@example.com"}'
```

### Get User Details

```bash
curl -X GET http://localhost:8000/users/user1
```

### Delete a User

```bash
curl -X DELETE http://localhost:8000/users/user1
```

### Create a Transaction

```bash
curl -X POST http://localhost:8000/transactions \
     -H "Content-Type: application/json" \
     -d '{"transactionId": "txn1", "userId": "user1", "amount": 100.50, "timestamp": "2024-12-13T10:00:00Z"}'
```

### List Transactions

```bash
curl -X GET "http://localhost:8000/transactions?userId=user1&startDate=2024-12-01&endDate=2024-12-12"
```

### Get Account Summary

```bash
curl -X GET http://localhost:8000/account-summary/user1
```

---

## Unit Testing

To run the unit tests, use the following command:

```bash
docker exec -it <container_id> pytest
```

Ensure your container is running before executing tests.

---

## Data Prepopulation

To prepopulate the database with sample data, use the provided script located in `scripts/prepopulate_data.py`. Execute it with the following command:

```bash
docker exec -it <container_id> python scripts/prepopulate_data.py
```
