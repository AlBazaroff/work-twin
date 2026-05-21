"""Enums related to integrations."""

from enum import Enum


class Integration(Enum):
    """Represents available integration services."""

    TELEGRAM = "telegram"
    SLACK = "slack"


class IntegrationStatus(Enum):
    """
    Represents status of separate integration.

    Statuses:
        PENDING: in the process of verification
        ACTIVE: verified that credentials able to work
        INACTIVE: for deactivated users
        EXPIRED: user's credentials expired
        REVOKED: user revoked credentials
    """

    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    REVOKED = "revoked"
