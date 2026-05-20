"""Authorization exceptions for integrations"""

from core.exception.base import BaseException


class BaseUserNotAuthorized(BaseException):
    """Error for not authorized exceptions in providers.

    Args:
        reason: reason of not authorized.
    """

    reason: str | None

    def __str__(self):
        if self.reason:
            return f"{self.message} (Reason {self.reason})"
        return self.message
