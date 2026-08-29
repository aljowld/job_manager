"""Core exception classes for the application."""


class ApplicationError(Exception):
    """Base exception for all application-level errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class DatabaseError(ApplicationError):
    """Exception for database-related errors."""

    def __init__(self, message: str = "Database error", code: str = "DATABASE_ERROR") -> None:
        super().__init__(message, code)


class ServiceUnavailableError(ApplicationError):
    """Exception for unavailable services."""

    def __init__(
        self, message: str = "Service unavailable", code: str = "SERVICE_UNAVAILABLE"
    ) -> None:
        super().__init__(message, code)
