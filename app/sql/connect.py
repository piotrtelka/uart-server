import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session
from app.settings import Settings

settings = Settings()

engine = create_engine(
    settings.database_url,
    pool_size=settings.pool_size,
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
