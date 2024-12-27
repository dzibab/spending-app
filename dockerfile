FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir uv && uv pip install --no-cache-dir --system -r requirements.txt

COPY /backend /app/backend
COPY .env /app/.env

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]