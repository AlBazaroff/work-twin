"""Test user service(CRUD operations)."""

import pytest
from uuid6 import uuid7

from user.models import User
from user.service import get, create, update, delete, get_or_create
from user.schemas import UserCreate, UserUpdate
from user.enums import UserStatus


@pytest.mark.asyncio
class TestUserCRUD:
    """Test User CRUDs."""

    async def _create_user(self, db_session, status=UserStatus.UNPAID) -> User:
        """Create User in DB for testing.

        Args:
            db_session: database session for creating
            status: status of user
        """
        user_id = uuid7()
        user = User(id=user_id, status=status)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        return user

    async def test_get_existing_user(self, db_session):
        """Test to get existing user from DB."""
        user = await self._create_user(db_session)

        result = await get(db_session=db_session, user_id=user.id)

        assert result is not None
        assert result.id == user.id
        assert result.status == user.status

    async def test_get_non_existent_user(self, db_session):
        """Test to try get non existent user, expected None."""
        result = await get(db_session=db_session, user_id=uuid7())

        assert result is None

    async def test_create_user(self, db_session):
        """Test creating a new user."""
        user_id = uuid7()
        user_in = UserCreate(id=user_id, status=UserStatus.UNPAID)

        result = await create(db_session=db_session, user_in=user_in)

        assert result is not None
        assert result.id == user_id
        assert result.status == UserStatus.UNPAID

    async def test_update_user(self, db_session):
        """Test updating an existing user."""
        user = await self._create_user(db_session)

        new_status = UserStatus.PAID
        user_in = UserUpdate(id=user.id, status=new_status)

        result = await update(db_session=db_session, user_in=user_in)

        assert result is not None
        assert result.id == user.id
        assert result.status == new_status

    async def test_delete_user(self, db_session):
        """Test deleting a user."""
        user = await self._create_user(db_session)

        result = await delete(db_session=db_session, user_id=user.id)

        assert result is not None
        assert result.id == user.id

        check = await get(db_session=db_session, user_id=user.id)
        assert check is None

    async def test_get_or_create_new_user(self, db_session):
        """Test get_or_create for a new user."""
        user_id = uuid7()

        result = await get_or_create(db_session=db_session, user_id=user_id)

        assert result is not None
        assert result.id == user_id
        assert result.status == UserStatus.UNPAID

    async def test_get_or_create_existing_user(self, db_session):
        """Test get_or_create for an existing user."""
        user = await self._create_user(db_session, status=UserStatus.PAID)

        result = await get_or_create(db_session=db_session, user_id=user.id)

        assert result is not None
        assert result.id == user.id
        assert result.status == UserStatus.PAID
