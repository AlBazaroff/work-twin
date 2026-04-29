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
