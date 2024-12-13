FROM python:3.12-slim

WORKDIR /app


COPY ./transaction_api ./transaction_api
COPY ./pyproject.toml  ./
COPY ./poetry.lock ./
COPY ./app.py ./
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8000

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
