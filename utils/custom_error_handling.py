from fastapi import HTTPException


class CustomError(HTTPException):
    def __init__(self, error: str, statuscode):
        super().__init__(status_code=statuscode, detail=error)
