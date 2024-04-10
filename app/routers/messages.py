from fastapi import APIRouter
from sqlalchemy import func
from sqlmodel import select, col

from app.api_utils.http_exceptions import BadRequest
from app.api_utils.pagination import Pagination
from app.sql.connect import SessionDependency
from app.sql.models import Message

router = APIRouter()


@router.get('/messages', response_model=Pagination[Message])
def messages(
    db: SessionDependency,
    limit: int = 100,
    page: int = 1,
):
    if limit <= 0:
        raise BadRequest(detail='limit must be greater than 0')
    if page <= 0:
        raise BadRequest(detail='page must be greater than 0')

    select_total = select(func.count(Message.id))
    total = (db.exec(select_total)).one()

    select_messages = select(Message)            \
        .order_by(col(Message.timestamp).desc()) \
        .limit(limit)                            \
        .offset(limit * (page - 1))

    rows = (db.exec(select_messages)).all()

    return Pagination.from_list(rows, limit, page, total)
