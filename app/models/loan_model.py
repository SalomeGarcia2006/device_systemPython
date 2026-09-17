from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship



class Loan(Base):
    __tablename__ = "loans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    loan_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    return_date = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    user = relationship(
        "User",
        back_populates="loans"
    )

    device = relationship(
        "Device",
        back_populates="loans"
    )