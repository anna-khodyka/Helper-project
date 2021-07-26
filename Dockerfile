FROM python:3

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY helper helper

CMD python helper/main.py