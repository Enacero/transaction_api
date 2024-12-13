FROM python:3.12-slim

WORKDIR /app


COPY ./transaction_api ./transaction_api
COPY ./pyproject.toml  ./
COPY ./poetry.lock ./
COPY ./scripts/populate_data/populate_data.py ./
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8000

CMD ["python3", "populate_data.py"]
