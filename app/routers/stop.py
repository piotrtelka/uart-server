from fastapi import APIRouter
from app.api_utils.http_responses import OK
from app.api_utils.uart_device_dependency import UARTDeviceDependency

router = APIRouter()


@router.get('/stop')
def stop(uart_device: UARTDeviceDependency):
    uart_device.cmd_stop()
    return OK()
