"""Base factory and provider classes."""

from abc import ABC, abstractmethod
from uuid import UUID

from config import Settings
from integrations.enums import Integration
from integrations.schemas import BaseCredentials


class BaseProvider(ABC):
    """Base provider interface for all data providers."""

    provider: Integration

    @classmethod
    @abstractmethod
    def from_settings(cls, settings: Settings):
        """Create provider instance from settings."""
        pass

    @abstractmethod
    async def get_identity(self, user_id: UUID, credentials: BaseCredentials):
        """Return identity in the provider service.

        Args:
            credentials: credentials to auth in the provider
        """
        pass


class SocialProvider(BaseProvider):
    """Base provider for social media services."""

    @abstractmethod
    async def fetch_chat_history(
        self,
        user_id: UUID,
        credentials: BaseCredentials,
        limit: int | None = None,
        *args,
        **kwargs,
    ):
        """Fetch chat history from provider service.

        Args:
            credentials: credentials to auth in the provider
            limit: limit of messages, if None - unlimited
        """
        pass

    @abstractmethod
    async def analyze_profile(
        self, user_id: UUID, credentials: BaseCredentials
    ):
        """Analyze user profile in provider service.

        Args:
            credentials: credentials to auth in the provider
        """
        pass
