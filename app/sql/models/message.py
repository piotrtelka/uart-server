from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class MessageIn(SQLModel):
    timestamp: int = Field(index=True, unique=True)
    pressure: float
    temperature: float
    velocity: float


class Message(MessageIn, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
