FROM python:3.9

WORKDIR /bot_backend

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["alembic", "upgrade", "head"]

CMD ["python3", "main.py"]