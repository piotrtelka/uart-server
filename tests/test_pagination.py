from pytest import raises
from app.api_utils.pagination import Pagination, PaginationData


def test_pagination_from_list_success():
    data = ["item1", "item2", "item3"]
    limit = 2
    page = 1
    total = len(data)
    pagination = Pagination.from_list(data, limit, page, total)

    assert pagination.data == data
    assert pagination.pagination == PaginationData(total=total, limit=limit, page=page, page_count=2)


def test_pagination_from_list_empty_data():
    data = []
    limit = 2
    page = 1
    total = 0
    pagination = Pagination.from_list(data, limit, page, total)

    assert pagination.data == []
    assert pagination.pagination == PaginationData(total=total, limit=limit, page=page, page_count=1)
