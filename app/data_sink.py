from abc import ABC, abstractmethod
from logging import warning
from sqlmodel import Session, select
from app.sql.connect import engine
from app.sql.models.message import MessageIn, Message


class DataSinkInterface(ABC):
    @abstractmethod
    def process(self, message: MessageIn):
        raise NotImplementedError()


class DataSink(DataSinkInterface):
    def process(self, message: MessageIn):
        with Session(engine) as db:
            if self.__already_exists(db, message):
                warning(f'Got duplicate record {message}')
                return
            message = Message.model_validate(message)
            db.add(message)
            db.commit()

    @staticmethod
    def __already_exists(db: Session, message: MessageIn):
        return db.exec(
            select(Message).where(Message.timestamp == message.timestamp)
        ).one_or_none() is not None
