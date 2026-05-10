from datetime import datetime

import uuid6
from sqlalchemy import Uuid, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    """
    Mixin, which generate base id field for most models.
    """

    id: Mapped[uuid6.UUID] = mapped_column(
        Uuid(native_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
        sort_order=-10,
    )


class TimeStampMixin:
    """
    Mixin, which generate base: created_at and updated_at field.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
