FROM python:3.14-slim

WORKDIR /api

COPY main.py .
COPY setup.py .
COPY .env.example .env
COPY helpers helpers

RUN ["mkdir", "/api/data"]
RUN ["touch", "/api/data/database.sqlite"]

COPY requirements.txt .
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

EXPOSE 8000

CMD [ "python", "./main.py"]