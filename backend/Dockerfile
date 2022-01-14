FROM python:3.8.10

WORKDIR /app_code
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
