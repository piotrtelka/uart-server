import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session
from app.settings import Settings

POOL_SIZE = int(os.getenv("POOL_SIZE", "4"))

engine = create_engine(
    Settings().database_url,
    pool_size=POOL_SIZE,
    max_overflow=0,
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
