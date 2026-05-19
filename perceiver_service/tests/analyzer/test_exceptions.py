"""Testing analyzer custom exceptions."""

import pytest

from analyzer.exceptions import EmbeddingNotFoundError
from core.exception.factory import EntityNotFoundError


@pytest.fixture
def embedding():
    return "fake_embedding"


class TestEmbeddingsExceptions:
    """Test embeddings exception classes and their behavior."""

    def test_embedding_not_found_uses__version_in_message(self, embedding):
        """
        Test EmbeddingNotFoundError formats the message with
        embedding name.
        """
        exc = EmbeddingNotFoundError(embedding)
        assert isinstance(exc, EntityNotFoundError)
        assert embedding in str(exc)
        assert "not found" in str(exc)
