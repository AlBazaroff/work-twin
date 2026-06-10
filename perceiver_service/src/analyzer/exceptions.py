"""Exceptions related with embeddings."""

from core.factory.exceptions import EntityNotFoundError


class EmbeddingNotFoundError(EntityNotFoundError):
    """Raise, when embedding not found in factory registry."""

    entity_name = "Embedding"
