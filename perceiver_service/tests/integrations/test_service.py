"""Test user integration service (CRUD operations)."""

from datetime import datetime

import pytest
from uuid import uuid4

from integrations.service import (
    get,
    create,
    create_or_update,
    update,
    delete,
)
from integrations.schemas import UserIntegrationCreate, UserIntegrationUpdate
from integrations.enums import Integration, IntegrationStatus
from user.models import User


@pytest.fixture
async def sample_user(db_session):
    user = User()
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def integration_data(sample_user):
    return {
        "user_id": sample_user.id,
        "integration": Integration.TELEGRAM,
        "credentials": {"api_key": "secret"},
        "status": IntegrationStatus.PENDING,
        "data": {"username": "test_user"},
    }


@pytest.mark.asyncio
class TestUserIntegrationCRUD:
    """Test UserIntegration CRUDs."""

    async def test_create_record(self, db_session, integration_data):
        """Test creating a new integration record."""
        # Remove 'data' from dictionary as it's not in the model
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        result = await create(
            db_session=db_session, integration_in=integration_in
        )

        assert result is not None
        assert result.user_id == integration_data["user_id"]
        assert result.integration == integration_data["integration"]
        assert result.credentials == integration_data["credentials"]
        assert result.status == integration_data["status"]

    async def test_get_existing_record(self, db_session, integration_data):
        """Test to get existing record from DB."""
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        created = await create(
            db_session=db_session, integration_in=integration_in
        )

        result = await get(db_session=db_session, integration_id=created.id)

        assert result is not None
        assert result.id == created.id

    async def test_get_non_existent_record(self, db_session):
        """Test to try get non existent record, expected None."""
        result = await get(db_session=db_session, integration_id=uuid4())

        assert result is None

    async def test_update_record(self, db_session, integration_data):
        """Test updating an existing record."""
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        created = await create(
            db_session=db_session, integration_in=integration_in
        )

        new_credentials = {"api_key": "updated_secret"}
        integration_update = UserIntegrationUpdate(
            id=created.id, user_id=created.user_id, credentials=new_credentials
        )
        result = await update(
            db_session=db_session, integration_in=integration_update
        )

        assert result is not None
        assert result.credentials == new_credentials

    async def test_create_or_update_create(self, db_session, integration_data):
        """Test create_or_update creates if not exists."""
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        result = await create_or_update(
            db_session=db_session,
            integration_in=integration_in,
            updated_at=datetime.now(),
        )

        assert result is not None
        assert result.user_id == integration_data["user_id"]

    async def test_create_or_update_update(self, db_session, integration_data):
        """Test create_or_update updates if exists."""
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        await create(db_session=db_session, integration_in=integration_in)

        new_credentials = {"api_key": "updated_secret_conflict"}
        integration_in.credentials = new_credentials

        result = await create_or_update(
            db_session=db_session,
            integration_in=integration_in,
            updated_at=datetime.now(),
        )

        assert result is not None
        assert result.credentials == new_credentials

    async def test_delete_record(self, db_session, integration_data):
        """Test deleting a record."""
        create_data = integration_data.copy()
        create_data.pop("data", None)

        integration_in = UserIntegrationCreate(**create_data)
        created = await create(
            db_session=db_session, integration_in=integration_in
        )

        result = await delete(db_session=db_session, integration_id=created.id)

        assert result is not None
        assert result.id == created.id

        # Verify it's gone
        check = await get(db_session=db_session, integration_id=created.id)
        assert check is None
