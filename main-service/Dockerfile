FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /var/www/weather-service

WORKDIR /var/www/weather-service

COPY requirements.txt .

RUN apt update && apt upgrade -y && apt install -y curl &&\
    pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]
