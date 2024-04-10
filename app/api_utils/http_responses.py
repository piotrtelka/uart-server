from fastapi import status
from fastapi.responses import JSONResponse


class OK(JSONResponse):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_200_OK, content={'detail': detail})
