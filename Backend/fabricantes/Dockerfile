FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev python3-dev libssl-dev && apt-get clean


RUN pip install --upgrade pip && pip install pipenv psycopg2


COPY Pipfile /app

COPY /src /app/src

RUN pipenv install --deploy --ignore-pipfile

EXPOSE 3001

ENV FLASK_APP="./src/main.py"

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=3001"]
