from logging import info, basicConfig, INFO
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from os import kill, getpid
from signal import SIGINT

from app.api_utils.uart_device_dependency import get_uart_device
from app.routers import include_routers


def worker():
    try:
        get_uart_device().work()
    except:
        kill(getpid(), SIGINT)


app = include_routers(FastAPI())
worker_thread = Thread(target=worker)
basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=INFO)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse('/docs')


@app.on_event("startup")
def startup_event():
    info('Starting worker thread')
    worker_thread.start()


@app.on_event("shutdown")
def app_shutdown():
    info('Stopping worker thread')
    get_uart_device().stop()
    worker_thread.join()
    info('Worker thread stopped')
