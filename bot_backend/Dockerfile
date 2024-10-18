FROM python:3.12

WORKDIR /bot_backend

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD alembic upgrade head && python3 main.py