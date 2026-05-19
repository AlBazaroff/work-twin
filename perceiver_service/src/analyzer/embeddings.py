"""Embeddings for storing information in vector store."""

from enum import Enum
from typing import Type

from langchain_core.embeddings import Embeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings

from config import get_settings
from core.factory.base import RegistryFactory
from .exceptions import EmbeddingNotFoundError

settings = get_settings()


class EmbeddingProvider(Enum):
    """Supported embeddings by service."""

    GOOGLE_V1 = "google_v1"
    GOOGLE_V2 = "google_v2"
    OLLAMA_NOMIC = "ollama_nomic"


class EmbeddingsFactory(RegistryFactory):
    """Factory for creating new embeddings models."""

    _registry: dict[EmbeddingProvider, tuple[Type[Embeddings], dict]] = {
        EmbeddingProvider.GOOGLE_V1: (
            GoogleGenerativeAIEmbeddings,
            {
                "model": "gemini-embedding-2-preview",
                "api_key": settings.google.api_key,
            },
        ),
        EmbeddingProvider.GOOGLE_V2: (
            GoogleGenerativeAIEmbeddings,
            {
                "model": "text-embedding-004",
                "api_key": settings.google.api_key,
            },
        ),
        EmbeddingProvider.OLLAMA_NOMIC: (
            OllamaEmbeddings,
            {"model": "nomic-embed-text"},
        ),
    }

    @classmethod
    def register(
        cls,
        embedding_cls: Type[Embeddings],
        emb_provider: EmbeddingProvider,
        *args,
        **kwargs,
    ):
        """Register new embedding in registry.

        Args:
            embedding_cls: class of Embedding
            emb_provider: embedding registered in provider
            **kwargs: kwargs for embedding class instance
        """
        cls._registry[emb_provider] = (embedding_cls, kwargs)

    @classmethod
    def get_entity(
        cls, embeddings: EmbeddingProvider, *args, **kwargs
    ) -> Embeddings:
        """Return embedding from registry.

        Args:
            embeddings: supported embeddings from SuppEmbeddings
        """
        if embeddings not in cls._registry:
            raise EmbeddingNotFoundError(embeddings.value)

        embed = cls._registry[embeddings]
        result = embed[0](**embed[1])
        return result
