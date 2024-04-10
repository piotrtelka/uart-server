from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4, UUID


class DeviceConfigIn(SQLModel):
    frequency: int
    debug: bool


class DeviceConfig(DeviceConfigIn, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
