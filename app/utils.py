# app/utils.py
from fastapi import HTTPException, status

def assert_resource_found(obj, name="Resource"):
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found")
    return obj
