FROM python:3.14-slim

WORKDIR /api

COPY requierments.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY setup.py .
COPY helpers helpers

EXPOSE 8000

CMD [ "python", ".\main.py"]