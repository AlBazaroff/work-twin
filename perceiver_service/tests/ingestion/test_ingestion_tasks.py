"""Tests for Celery ingestion task payload handling."""

from unittest.mock import AsyncMock, MagicMock, patch

from uuid6 import uuid7

from user.enums import UserStatus


class TestIngestUserIntegrationDataTask:
    @patch("ingestion.tasks.analyze_user_integration_data")
    @patch("ingestion.tasks.get_db")
    @patch("ingestion.tasks.IngestionService")
    def test_schedules_analysis_for_paid_user(
        self,
        mock_service_cls,
        mock_get_db,
        mock_analyze_task,
        user_integration_payload,
    ):
        """Test adding analysis task for paid user."""
        from ingestion.tasks import ingest_user_integration_data

        integration_id = uuid7()

        mock_user = MagicMock()
        mock_user.id = user_integration_payload.user_id
        mock_user.status = UserStatus.PAID
        mock_integration = MagicMock()
        mock_integration.id = integration_id
        mock_integration.integration = user_integration_payload.integration

        mock_response = MagicMock(user=mock_user, integration=mock_integration)
        mock_service = AsyncMock()
        mock_service.pass_user_integration_data = AsyncMock(
            return_value=mock_response
        )
        mock_service_cls.return_value = mock_service

        mock_session = AsyncMock()
        mock_get_db.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_get_db.return_value.__aexit__ = AsyncMock(return_value=None)

        ingest_user_integration_data.run(
            user_integration_payload.model_dump_json()
        )

        mock_analyze_task.delay.assert_called_once()
        delay_arg = mock_analyze_task.delay.call_args[0][0]
        assert str(integration_id) in delay_arg

    @patch("ingestion.tasks.analyze_user_integration_data")
    @patch("ingestion.tasks.get_db")
    @patch("ingestion.tasks.IngestionService")
    def test_skips_analysis_for_unpaid_user(
        self,
        mock_service_cls,
        mock_get_db,
        mock_analyze_task,
        user_integration_payload,
    ):
        """Test skip adding analysis task for unpaid user."""
        from ingestion.tasks import ingest_user_integration_data

        mock_user = MagicMock(status=UserStatus.UNPAID)
        mock_response = MagicMock(
            user=mock_user, integration=MagicMock(id=uuid7())
        )
        mock_service = AsyncMock()
        mock_service.pass_user_integration_data = AsyncMock(
            return_value=mock_response
        )
        mock_service_cls.return_value = mock_service
        mock_get_db.return_value.__aenter__ = AsyncMock(
            return_value=AsyncMock()
        )
        mock_get_db.return_value.__aexit__ = AsyncMock(return_value=None)

        ingest_user_integration_data.run(
            user_integration_payload.model_dump_json()
        )

        mock_analyze_task.delay.assert_not_called()
