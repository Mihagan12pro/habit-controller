from fastapi import HTTPException


def check_errors(result, code: int):
    if isinstance(result, str):
        raise HTTPException(status_code=code, detail=result)
