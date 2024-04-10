from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginationData(BaseModel):
    total: int
    limit: int
    page: int
    page_count: int


class Pagination(BaseModel, Generic[T]):
    pagination: PaginationData | None
    data: list[T]

    @classmethod
    def from_list(cls, data: list[T], limit: int, page: int, total: int):
        return cls(
            data=data,
            pagination=PaginationData(
                total=total,
                limit=limit,
                page=page,
                page_count=total // limit + 1
            )
        )
