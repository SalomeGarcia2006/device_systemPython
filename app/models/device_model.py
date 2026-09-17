from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = "devices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    serial_number = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    device_type = Column(
        String,
        nullable=False
    )

    brand = Column(
        String,
        nullable=True
    )

    is_available = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    loans = relationship(
        "Loan",
        back_populates="device"
    )


