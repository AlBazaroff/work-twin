from enum import Enum


class KnowledgeScope(Enum):
    """
    Define privacy of knowledge.

    Scopes:
        GLOBAL: available to refer in every chat;
        PRIVATE: available to refer only in chat with
                 specific user
    """

    GLOBAL = "global"
    PRIVATE = "private"


class KnowledgeSourceType(Enum):
    """
    Define source of message.

    Source types:
        PRIVATE_CHAT: messages from private chats
        GROUP_CHAT: messages from group chats
    """

    PRIVATE_CHAT = "private chat"
    GROUP_CHAT = "group chat"


class UserStatus(Enum):
    """
    Represent status of user account.

    Statuses:
        PAID: successfully paid
        UNPAID: unpaid
        DEACTIVATED: deactivated account
    """

    PAID = "paid"
    UNPAID = "unpaid"
    DEACTIVATED = "deactivated"


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
