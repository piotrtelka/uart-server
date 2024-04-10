# UART-SERVER

Server with HTTP API that communicates with UART device.

## Preparation:

1. create virtual environment: `python -m venv .venv`
2. activate virtual environment: `source .venv/bin/acitvate`
3. install requirements: `python -m pip install -r requirements.txt`
4. create database file: `sqlite3 database.db`
5. create .env file: `cp .env.example .env`

## Running the server:

To run the server serial device is needed. For development purposes I created uart-device repo that emulates serial device using `socat` command.
For details go here: https://github.com/piotrtelka/uart-device. The easiest way to start both tools is to put them in same folder and run with default config.

1. run uart-device
2. run startup.sh script `./startup.sh`. It automatically runs the server and database migrations.

## Configuration:

uart-server can be configured using env vars or .env file. List of supported variables:
- `DATABASE_URL` - path to database. Defaults to `sqlite:///database.db`
- `DEVICE_PORT` - path to uart-device port. Defaults to `../client_port`
- `BAUD_RATE` - ports baud rate. Defaults to `115000`
- `HOST` - API host. Defaults to `localhost`
- `PORT` - API port. Defaults to `7100`

## Swagger:

Interactive Swagger UI is available under `/` and `/docs`

## Database migrations:

After making any changes in [models](app%2Fsql%2Fmodels) you can generate new database migration using alembic:
- `python -m alembic revision --autogenerate -m "<message>"`

After that you can apply generated migration:
- `python -m alembic upgrade head`

## API

All the endpoints are implemented in accordance with the guidelines from task description.
