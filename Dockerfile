FROM python:3

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pipenv install --system --deploy

COPY helper /app/helper

CMD python /app/helper/main.py