FROM python:3.11-slim

WORKDIR /api

COPY main.py .
COPY setup.py .
COPY .env.example .env
COPY helpers helpers
COPY requirements.txt .

RUN ["mkdir", "/api/data"]
RUN ["touch", "/api/data/database.sqlite"]

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "gcc", "python3-dev"] 

RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

RUN ["apt-get", "purge", "-y", "--auto-remove", "gcc", "python3-dev"]
RUN ["rm", "-rf", "/var/lib/apt/lists/*"]

EXPOSE 8000

CMD [ "python", "./main.py"]