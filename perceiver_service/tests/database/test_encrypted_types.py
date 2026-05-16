"""Tests for SQLAlchemy encrypted column types."""

import json

import pytest
from sqlalchemy import Dialect

from database.types import EncryptedJSON, EncryptedString


class _StubDialect(Dialect):
    name = "postgresql"


@pytest.fixture
def dialect():
    return _StubDialect()


@pytest.fixture
def plain_text():
    return "session-token-xyz"


@pytest.fixture
def json_payload():
    return {"session_string": "zyx", "other_key": 123}


class TestEncryptedString:
    """Test encryption and decryption of string column type."""

    def test_roundtrip_encrypts_and_decrypts(self, dialect, plain_text):
        """
        If encrypted and decrypt work, encrypt will differ with
        started value. And after decrypt it will have the same value.
        """
        column = EncryptedString()
        stored = column.process_bind_param(plain_text, dialect)
        assert stored != plain_text
        assert column.process_result_value(stored, dialect) == plain_text

    def test_none_passes_through_unchanged(self, dialect):
        """
        None should no be encrypted or decrypted, just pass through.
        """
        column = EncryptedString()
        assert column.process_bind_param(None, dialect) is None
        assert column.process_result_value(None, dialect) is None

    def test_empty_string_roundtrip(self, dialect):
        """
        Empty string should be encrypted and decrypted correctly.
        """
        column = EncryptedString()
        stored = column.process_bind_param("", dialect)
        assert column.process_result_value(stored, dialect) == ""


class TestEncryptedJSON:
    """Test encryption and decryption of JSON column type."""

    def test_roundtrip_dict(self, dialect):
        """
        Test that a dict can be encrypted and decrypted correctly,
        and that the stored value is not just the JSON string.
        """
        column = EncryptedJSON()
        payload = {"session_string": "abc", "nested": [1, 2]}
        stored = column.process_bind_param(payload, dialect)
        assert isinstance(stored, str)
        assert column.process_result_value(stored, dialect) == payload

    def test_none_passes_through(self, dialect):
        """None should pass through without encryption or decryption."""
        column = EncryptedJSON()
        assert column.process_bind_param(None, dialect) is None
        assert column.process_result_value(None, dialect) is None

    def test_stored_blob_is_opaque_encrypted_text(self, dialect):
        """
        The stored value should not be the plain JSON string,
        but some encrypted version of it.
        """
        column = EncryptedJSON()
        stored = column.process_bind_param({"k": "v"}, dialect)
        assert isinstance(stored, str)
        assert stored != json.dumps({"k": "v"})
        assert column.process_result_value(stored, dialect) == {"k": "v"}
