"""Test personality dna service(CRUD operations)."""

import pytest
from uuid6 import uuid7

from personality_dna.models import PersonalityDNA
from personality_dna.service import (
    get,
    get_active_by_user_id,
    create,
    update,
    delete,
)
from personality_dna.schemas import PersonalityDNACreate, PersonalityDNAUpdate
from user.models import User


@pytest.mark.asyncio
class TestPersonalityDNACRUD:
    """Test PersonalityDNA CRUDs."""

    async def test_get_existing_record(
        self, db_session, active_personality_dna
    ):
        """Test to get existing record from DB."""
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()

        result = await get(
            db_session=db_session, personality_id=active_personality_dna["id"]
        )

        assert result is not None
        assert result.id == active_personality_dna["id"]
        assert result.is_active is active_personality_dna["is_active"]

    async def test_get_non_existent_record(self, db_session):
        """Test to try get non existent record, expected None."""
        result = await get(db_session=db_session, personality_id=999)

        assert result is None

    async def test_get_active_by_user_id_success(
        self, db_session, active_personality_dna
    ):
        """Test get active by user_id with existed personality."""
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()

        result = await get_active_by_user_id(
            db_session=db_session, user_id=active_personality_dna["user_id"]
        )

        assert result is not None
        assert result.user_id == active_personality_dna["user_id"]
        assert result.is_active is True

    async def test_get_active_by_user_id_ignores_inactive(
        self, db_session, active_personality_dna
    ):
        """
        Test try to get active by user_id with inactive personalities.
        Expected None.
        """
        active_personality_dna["is_active"] = False
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()

        result = await get_active_by_user_id(
            db_session=db_session, user_id=active_personality_dna["user_id"]
        )

        assert result is None

    async def test_get_active_by_wrong_user_id(
        self, db_session, active_personality_dna
    ):
        """
        Test try to get active by wrong user_id.
        Expected None.
        """
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()

        result = await get_active_by_user_id(
            db_session=db_session, user_id=uuid7()
        )

        assert result is None

    async def test_create_record(self, db_session):
        """Test creating a new personality record."""
        user = User()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        personality_in = PersonalityDNACreate(
            user_id=user.id,
            style_markers={"style": "cool"},
            version=1,
        )
        result = await create(
            db_session=db_session, personality_in=personality_in
        )

        assert result is not None
        assert result.user_id == user.id
        assert result.style_markers == {"style": "cool"}
        assert result.version == 1

    async def test_update_record(self, db_session, active_personality_dna):
        """Test updating an existing record."""
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()
        await db_session.refresh(dna)

        personality_in = PersonalityDNAUpdate(
            id=dna.id,
            style_markers={"style": "new-style"},
        )
        result = await update(
            db_session=db_session, personality_in=personality_in
        )

        assert result is not None
        assert result.style_markers == {"style": "new-style"}
        assert result.version == active_personality_dna["version"]

    async def test_delete_record(self, db_session, active_personality_dna):
        """Test deleting a record."""
        dna = PersonalityDNA(**active_personality_dna)
        db_session.add(dna)
        await db_session.commit()

        result = await delete(db_session=db_session, personality_id=dna.id)

        assert result is not None
        assert result.id == dna.id

        # Verify it's gone
        check = await get(db_session=db_session, personality_id=dna.id)
        assert check is None
