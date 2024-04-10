FROM python:3.10-slim-buster

WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./app /src/app
COPY ./startup.sh /src/startup.sh
COPY ./alembic.ini /src/alembic.ini
COPY ./alembic /src/alembic

CMD ./startup.sh
