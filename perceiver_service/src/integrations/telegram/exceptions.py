"""Telegram auth related exceptions"""

from integrations.exceptions import BaseUserNotAuthorized


class TelegramUserNotAuthorized(BaseUserNotAuthorized):
    """Exception used, when telegram session not authorized."""

    message = "[Telegram] User {user} is not authorized"

    def __init__(
        self,
        user: str | None = None,
        message: str | None = None,
        reason: str | None = None,
    ):
        """Initialize telegram user not authorized error.

        Args:
            user: user for default template value.
            message: new message for exception(don't use user arg)
            reason: reason of not authorized.
        """
        if message:
            self.message = message
        elif user:
            self.message = self.message.format(user=user)

        self.reason = reason
        super().__init__(self.message)
