"""Tests for factory exceptions."""

from core.factory.exceptions import EntityNotFoundError


class TestEntityNotFoundError:
    """Tests for EntityNotFoundError."""

    def test_message_formatting(self):
        """Test that the error message is correctly formatted."""

        class TestEntity(EntityNotFoundError):
            entity_name = "TestEntity"

        exc = TestEntity("test_name")
        assert str(exc) == "TestEntity 'test_name' not found"
        assert exc.message == "TestEntity 'test_name' not found"
