"""Core exception classes for the application."""


class ApplicationError(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseError(ApplicationError):
    """Exception for database-related errors."""

    def __init__(
        self,
        message: str = "Database error",
        code: str = "DATABASE_ERROR",
        status_code: int = 400,
    ) -> None:
        super().__init__(message, code, status_code)


class ServiceUnavailableError(ApplicationError):
    """Exception for unavailable services."""

    def __init__(
        self,
        message: str = "Service unavailable",
        code: str = "SERVICE_UNAVAILABLE",
        status_code: int = 503,
    ) -> None:
        super().__init__(message, code, status_code)


class ProfileNotFoundError(ApplicationError):
    """Raised when the single-user profile has not been created yet."""

    def __init__(self, message: str = "User profile has not been created yet") -> None:
        super().__init__(message, "PROFILE_NOT_FOUND", 404)
