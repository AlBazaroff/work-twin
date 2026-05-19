"""Base exceptions for the perceiver service."""


class BaseException(Exception):
    """Base exception for all service errors."""

    message: str = "An unexpected error occurred"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)
