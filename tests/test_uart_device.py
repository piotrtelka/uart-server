import time
from threading import Thread

from app.api_utils.http_exceptions import Timeout
from app.data_sink import DataSinkInterface
from app.serial_port import SerialPortInterface
from app.sql.models.message import MessageIn
from app.uart_device import UARTDevice
import pytest


class MockSerialPort(SerialPortInterface):
    def __init__(self, data_to_send=None):
        self.written_data = []
        self.data_to_send = data_to_send if data_to_send else []

    def write(self, data):
        self.written_data.append(data)

    def flush(self):
        pass

    def readline(self) -> str:
        if len(self.data_to_send) > 0:
            return self.data_to_send.pop(0)
        return ''


class MockDataSink(DataSinkInterface):
    def __init__(self):
        self.processed_messages = []

    def process(self, message: MessageIn):
        self.processed_messages.append(message)


def work_in_thread(device: UARTDevice):
    Thread(target=lambda: device.work(), daemon=True).start()


def test_valid_message():
    serial_mock = MockSerialPort(['$1.2,3.4,5.6\n'])
    data_sink_mock = MockDataSink()
    device = UARTDevice(serial_mock, data_sink_mock)

    work_in_thread(device)
    time.sleep(0.1)
    device.stop()

    assert not device.is_working
    assert len(data_sink_mock.processed_messages) == 1

    message = data_sink_mock.processed_messages[0]

    assert message.pressure == 1.2
    assert message.temperature == 3.4
    assert message.velocity == 5.6


def test_cmd_stop_timeout():
    serial_mock = MockSerialPort()
    data_sink_mock = MockDataSink()
    device = UARTDevice(serial_mock, data_sink_mock)

    with pytest.raises(Timeout):
        device.cmd_stop()


def test_cmd_start_timeout():
    serial_mock = MockSerialPort()
    data_sink_mock = MockDataSink()
    device = UARTDevice(serial_mock, data_sink_mock)

    with pytest.raises(Timeout):
        device.cmd_start()


def test_cmd_configure_timeout():
    serial_mock = MockSerialPort()
    data_sink_mock = MockDataSink()
    device = UARTDevice(serial_mock, data_sink_mock)

    with pytest.raises(Timeout):
        device.cmd_configure(10, False)
