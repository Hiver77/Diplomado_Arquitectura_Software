FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask psycopg2-binary pika

COPY command_service.py .

CMD ["python", "command_service.py"]