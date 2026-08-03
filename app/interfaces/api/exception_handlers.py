from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.exceptions.request_exceptions import RequestAlreadyExistsError, RequestNotFoundError
from app.domain.exceptions.request_exceptions import DomainError, DuplicateExternalIdentifierError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        if isinstance(exc, DuplicateExternalIdentifierError):
            status_code = status.HTTP_409_CONFLICT
        return JSONResponse(status_code=status_code, content={"detail": "invalid request"})

    @app.exception_handler(RequestAlreadyExistsError)
    async def handle_application_conflict(_: Request, __: RequestAlreadyExistsError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "request already exists"})

    @app.exception_handler(RequestNotFoundError)
    async def handle_not_found(_: Request, __: RequestNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "request not found"})
