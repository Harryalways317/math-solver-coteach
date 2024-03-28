FROM python:3.12-slim

LABEL authors="harishvadaparty"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["python", "main.py"]
