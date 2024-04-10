from fastapi import APIRouter
from app.sql.connect import SessionDependency
from app.sql.models.device_config import DeviceConfigIn, DeviceConfig
from app.api_utils.uart_device_dependency import UARTDeviceDependency

router = APIRouter()


@router.put('/configure', response_model=DeviceConfig)
def configure(config: DeviceConfigIn, uart_device: UARTDeviceDependency, db: SessionDependency):
    config = DeviceConfig.model_validate(config)
    uart_device.cmd_configure(config.frequency, config.debug)
    db.add(config)
    db.commit()
    db.refresh(config)
    return config
