from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routers import accounting, accounts, auth, bank_accounts, categories, customers, health, inventory, payments, products, purchase_invoices, reports, sale_invoices, suppliers, tags
from app.schemas.common import fail


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.3.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors_origin_list],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.api_v1_prefix)
    app.include_router(auth.router, prefix=settings.api_v1_prefix)
    app.include_router(customers.router, prefix=settings.api_v1_prefix)
    app.include_router(suppliers.router, prefix=settings.api_v1_prefix)
    app.include_router(categories.router, prefix=settings.api_v1_prefix)
    app.include_router(tags.router, prefix=settings.api_v1_prefix)
    app.include_router(products.router, prefix=settings.api_v1_prefix)
    app.include_router(bank_accounts.router, prefix=settings.api_v1_prefix)
    app.include_router(purchase_invoices.router, prefix=settings.api_v1_prefix)
    app.include_router(sale_invoices.router, prefix=settings.api_v1_prefix)
    app.include_router(payments.router, prefix=settings.api_v1_prefix)
    app.include_router(inventory.router, prefix=settings.api_v1_prefix)
    app.include_router(accounts.router, prefix=settings.api_v1_prefix)
    app.include_router(accounting.router, prefix=settings.api_v1_prefix)
    app.include_router(reports.router, prefix=settings.api_v1_prefix)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=fail(code="http_error", message=str(exc.detail)),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=fail(code="validation_error", message="Request validation failed", details={"errors": exc.errors()}),
        )

    # Catch-all for any unhandled exception. When an unhandled error occurs,
    # the response is sent by ServerErrorMiddleware directly through the raw
    # ASGI send, bypassing CORSMiddleware entirely. So a bare 500 response
    # would still fail the browser's CORS check. We therefore attach the CORS
    # headers ourselves (mirroring CORSMiddleware's simple-request behaviour
    # for the configured allow-list) and return a structured JSON error so
    # that server failures are actually visible in the browser instead of a
    # misleading "No 'Access-Control-Allow-Origin'" message.
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, _exc: Exception) -> JSONResponse:
        headers: dict[str, str] = {}
        origin = request.headers.get("origin")
        if origin and origin in settings.cors_origin_list:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Vary"] = "Origin"
            headers["Access-Control-Allow-Credentials"] = "true"
        return JSONResponse(
            status_code=500,
            content=fail(code="internal_error", message="Internal server error"),
            headers=headers or None,
        )

    return app


app = create_app()
