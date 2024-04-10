from typing import Annotated
from fastapi import Depends

from app.data_sink import DataSink
from app.serial_port import SerialPort
from app.settings import Settings
from app.uart_device import UARTDevice


def get_uart_device() -> UARTDevice:
    if not hasattr(get_uart_device, "uart_device"):
        settings = Settings()

        get_uart_device.uart_device = UARTDevice(
            SerialPort(port=settings.device_port, baud_rate=settings.baud_rate, timeout=1),
            DataSink()
        )

    return get_uart_device.uart_device


UARTDeviceDependency = Annotated[UARTDevice, Depends(get_uart_device)]
