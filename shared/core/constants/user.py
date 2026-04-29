from enum import Enum


class UserStatus(Enum):
    """
    Represent status of user account.

    Statuses:
        PAID: successfully paid
        UNPAID: unpaid
        DEACTIVATED: deactivated account
    """

    PAID = "paid", "Paid"
    UNPAID = "unpaid", "Unpaid"
    DEACTIVATED = "deactivated", "Deactivated"


class Integrity(Enum):
    """Represents available integrity services."""

    TELEGRAM = "telegram", "Telegram"
    SLACK = "slack", "Slack"


class IntegrityStatus(Enum):
    """
    Represents status of separate integrity.

    Statuses:
        PENDING: in the process of verification
        ACTIVE: verified that credentials able to work
        INACTIVE: for deactivated users
        EXPIRED: user's credentials expired
        REVOKED: user revoked credentials
    """

    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    EXPIRED = "expired", "Expired"
    REVOKED = "revoked", "Revoked"
