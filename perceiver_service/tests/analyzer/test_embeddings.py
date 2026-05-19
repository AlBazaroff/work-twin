"""Tests for embeddings module."""

import pytest
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from analyzer.embeddings import EmbeddingProvider, EmbeddingsFactory


@pytest.fixture
def valid_embed_data():
    """Return valid embedding data"""
    provider = EmbeddingProvider.GOOGLE_V2
    model = "text-embedding-004"
    api_key = "fake-api-key"
    return {
        "provider": provider,
        "provider_cls": GoogleGenerativeAIEmbeddings,
        "kwargs": {
            "model": model,
            "api_key": api_key,
        },
    }


class TestEmbeddingFactory:
    """Test behavior embedding factory"""

    def test_succeed_register_valid_embedding(self, valid_embed_data):
        """Test that register must be succeed with valid embed data"""
        EmbeddingsFactory.register(
            valid_embed_data["provider_cls"],
            valid_embed_data["provider"],
            **valid_embed_data["kwargs"],
        )
        assert EmbeddingsFactory._registry[valid_embed_data["provider"]] == (
            valid_embed_data["provider_cls"],
            valid_embed_data["kwargs"],
        )
