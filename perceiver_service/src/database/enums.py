from enum import Enum


class KnowledgeScope(Enum):
    """
    Define privacy of knowledge.

    Scopes:
        GLOBAL: available to refer in every chat;
        PRIVATE: available to refer only in chat with
                 specific user
    """

    GLOBAL = "global", "Global"
    PRIVATE = "private", "Private"


class KnowledgeSourceType(Enum):
    """
    Define source of message.

    Source types:
        PRIVATE_CHAT: messages from private chats
        GROUP_CHAT: messages from group chats
    """

    PRIVATE_CHAT = "private chat", "Private chat"
    GROUP_CHAT = "group chat", "Group chat"


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
