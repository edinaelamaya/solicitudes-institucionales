class DomainError(Exception):
    """Base exception for domain errors."""


class InvalidRequestCategoryError(DomainError):
    """Raised when a request category is not allowed."""


class InvalidRequestPriorityError(DomainError):
    """Raised when a request priority is not allowed."""


class InvalidRequestStatusError(DomainError):
    """Raised when a request status is not allowed."""


class DuplicateExternalIdentifierError(DomainError):
    """Raised when a request already exists for the external identifier."""


class RequestNotFoundError(DomainError):
    """Raised when the requested entity does not exist."""
