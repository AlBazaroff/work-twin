"""Exceptions related with embeddings."""

from core.exception.factory import EntityNotFoundError


class EmbeddingNotFoundError(EntityNotFoundError):
    """Raise, when embedding not found in factory registry."""

    entity_name = "Embedding"
