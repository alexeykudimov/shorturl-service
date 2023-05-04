import logging
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from src.misc.database import ModelBase

from src.config.settings import settings

logger = logging.getLogger(__name__)


class Link(ModelBase):
    __tablename__ = 'link'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    shortened_id = Column(String(63), nullable=False, unique=True)
    full_link = Column(String(511), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def shortened_link(self):
        return f"{settings.BASE_URL}/{self.shortened_id}"
    
    def __str__(self):
        return self.shortened_id
    