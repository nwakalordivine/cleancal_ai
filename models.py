from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, Uuid, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
import uuid
from database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default='pending')
    image_url = Column(Text)
    location = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Uuid, nullable=False)
    votes = Column(Integer, default=0)
    severity = Column(Text)
    type = Column(Text)
    category = Column(Text)
    tags = Column(ARRAY(String))
    is_resolved = Column(Boolean, default=False)