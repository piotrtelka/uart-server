from abc import ABC, abstractmethod
from serial import Serial


class SerialPortInterface(ABC):
    @abstractmethod
    def write(self, data: bytes):
        raise NotImplementedError()

    @abstractmethod
    def flush(self):
        raise NotImplementedError()

    @abstractmethod
    def readline(self) -> str:
        raise NotImplementedError()


class SerialPort(SerialPortInterface):
    def __init__(self, port: str, baud_rate: int, timeout: float):
        self.serial = Serial(port=port, baudrate=baud_rate, rtscts=True, dsrdtr=True, timeout=timeout)

    def write(self, data: bytes):
        self.serial.write(data)

    def flush(self):
        self.serial.flush()

    def readline(self) -> str:
        return self.serial.readline().decode('utf-8')
