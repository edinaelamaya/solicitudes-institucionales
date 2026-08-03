class ApplicationError(Exception):
    """Base exception for application failures."""


class RequestAlreadyExistsError(ApplicationError):
    """Raised when the external identifier is duplicated."""


class RequestNotFoundError(ApplicationError):
    """Raised when a request cannot be found."""
