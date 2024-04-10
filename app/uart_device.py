from abc import ABC, abstractmethod
from logging import warning, info
from re import match
from threading import Lock
from app.data_sink import DataSinkInterface
from time import time_ns

from app.api_utils.http_exceptions import Timeout, BadRequest
from app.serial_port import SerialPortInterface
from app.sql.models.message import MessageIn


class UARTDevice:
    def __init__(self, serial: SerialPortInterface, data_sink: DataSinkInterface, cmd_timeout: float = 1.0):
        self.serial = serial
        self.data_sink = data_sink
        self.cmd_timeout = cmd_timeout
        self.is_working = True
        self.mutex = Lock()

    def work(self):
        while self.is_working:
            with self.mutex:
                message = self.__readline()

            if is_valid(message):
                self.__process_message(message)
            elif len(message) > 0:
                warning(f'Got invalid message {message}')

    def cmd_stop(self):
        info('Sending STOP command to UART device')

        with self.mutex:
            self.__write(b'$1\n')
            response = self.__wait_for_response('1')

            if response != 'ok':
                raise BadRequest(detail=response)

        info('STOP sent successfully')

    def cmd_start(self):
        info('Sending START command to UART device')
        with self.mutex:
            self.__write(b'$0\n')
            response = self.__wait_for_response('0')

            if response != 'ok':
                raise BadRequest(detail=response)
        info('START sent successfully')

    def cmd_configure(self, frequency: int, debug: bool):
        debug = 'true' if debug else 'false'
        cmd = f'$2,{frequency},{debug}\n'.encode('utf-8')

        info(f'Sending CONFIGURE command to UART device ({cmd})')
        with self.mutex:
            self.__write(cmd)
            response = self.__wait_for_response('2')

            if response != 'ok':
                raise BadRequest(detail=response)
        info('CONFIGURE sent successfully')

    def stop(self):
        self.is_working = False

    def __process_message(self, message: str):
        timestamp = time_ns()
        pressure, temperature, velocity = extract_data(message)

        self.data_sink.process(MessageIn(
            pressure=pressure,
            temperature=temperature,
            velocity=velocity,
            timestamp=timestamp
        ))

    def __write(self, out: bytes):
        self.serial.write(out)
        self.serial.flush()

    def __readline(self):
        return self.serial.readline()

    def __wait_for_response(self, command_prefix: str) -> str:
        start = time_ns()
        while True:
            now = time_ns()
            delta = (now - start) / 1000000000.0

            if delta > self.cmd_timeout:
                raise Timeout()

            message = self.__readline()
            if is_valid(message):
                self.__process_message(message)
                continue

            result = get_result(message, command_prefix)

            if result:
                return result


def is_valid(message: str) -> bool:
    return match(r'^\$\d+\.\d+,\d+\.\d+,\d+\.\d+\n$', message) is not None


def extract_data(message: str) -> tuple[float, float, float]:
    message = message.replace('$', '').replace('\n', '')
    values = message.split(',')
    return float(values[0]), float(values[1]), float(values[2])


def get_result(message: str, command_prefix: str) -> str | None:
    if not message.startswith(f'${command_prefix},'):
        return None
    if not message.endswith('\n'):
        return None
    return message.replace(f'${command_prefix},', '').replace('\n', '')
