from fastapi import status
from fastapi.exceptions import HTTPException


def _define_exception(name: str, status_code: status):
    __class__ = HTTPException

    def init(self, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)

    return type(name, (HTTPException, ), {
        "__init__": init,
    })


BadRequest = _define_exception("BadRequest", status.HTTP_400_BAD_REQUEST)
Timeout = _define_exception("Timeout", status.HTTP_408_REQUEST_TIMEOUT)
