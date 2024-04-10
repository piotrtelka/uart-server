from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select, Session, col

from app.sql.connect import SessionDependency
from app.sql.models import Message, DeviceConfig

router = APIRouter()


class Mean(BaseModel):
    pressure: float
    temperature: float
    velocity: float


class DeviceResponse(BaseModel):
    debug: bool
    curr_config: DeviceConfig | None
    mean_last_10: Mean
    latest: Message | None


@router.get('/device', response_model=DeviceResponse)
def device(
    db: SessionDependency
):
    messages = get_last_messages(db)

    return DeviceResponse(
        debug=False,
        curr_config=get_current_config(db),
        mean_last_10=calc_mean(messages),
        latest=messages[0] if len(messages) > 0 else None
    )


def get_current_config(db: Session) -> DeviceConfig | None:
    stmt = select(DeviceConfig)                        \
        .order_by(col(DeviceConfig.created_at).desc()) \
        .limit(1)

    return db.exec(stmt).one_or_none()


def get_last_messages(db: Session) -> list[Message]:
    stmt = select(Message)                       \
        .order_by(col(Message.timestamp).desc()) \
        .limit(10)

    return list(db.exec(stmt).all())


def calc_mean(messages: list[Message]) -> Mean:
    def mean(data: list[float]) -> float:
        if len(data) == 0:
            return 0
        return sum(data) / len(data)

    return Mean(
        pressure=mean(list(map(lambda message: message.pressure, messages))),
        temperature=mean(list(map(lambda message: message.temperature, messages))),
        velocity=mean(list(map(lambda message: message.velocity, messages))),
    )
