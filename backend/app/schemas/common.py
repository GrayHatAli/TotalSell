from typing import Any, Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class ErrorInfo(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool
    data: DataT | None = None
    meta: dict[str, Any] | None = None
    error: ErrorInfo | None = None


def ok(data: DataT | None = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"success": True, "data": data, "meta": meta, "error": None}


def fail(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"success": False, "data": None, "meta": None, "error": {"code": code, "message": message, "details": details}}

