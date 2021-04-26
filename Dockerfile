FROM python:3.6-slim-buster
RUN apt-get -y update && apt-get install -y sqlite3 libsqlite3-dev

COPY ./app /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]


