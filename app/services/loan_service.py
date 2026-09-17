from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


def get_loans(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
):
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
    )

    if status:
        query = query.filter(Loan.status == status)

    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))

    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))

    return query.all()


def get_loan(db: Session, loan_id: int):
    return (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .filter(Loan.id == loan_id)
        .first()
    )


def create_loan(db: Session, data: LoanCreate):
    # Verificar que el usuario exista
    user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if not user:
        return "user_not_found"

    # Verificar que el dispositivo exista
    device = (
        db.query(Device)
        .filter(Device.id == data.device_id)
        .first()
    )

    if not device:
        return "device_not_found"

    # Verificar disponibilidad
    if not device.is_available:
        return "device_unavailable"

    # Crear préstamo
    loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        loan_date=datetime.utcnow(),
        status="active",
    )

    # Cambiar disponibilidad del dispositivo
    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def return_loan(db: Session, loan_id: int):
    loan = (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )

    if not loan:
        return "loan_not_found"

    # Evitar devolver un préstamo que ya fue devuelto
    if loan.status == "returned" or loan.return_date is not None:
        return "already_returned"

    device = (
        db.query(Device)
        .filter(Device.id == loan.device_id)
        .first()
    )

    loan.return_date = datetime.utcnow()
    loan.status = "returned"

    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)

    return loan


def get_loan_details(db: Session):
    return (
        db.query(
            Loan.id,
            Loan.user_id,
            User.name.label("user_name"),
            User.email.label("user_email"),
            Loan.device_id,
            Device.name.label("device_name"),
            Device.serial_number,
            Device.device_type,
            Loan.loan_date,
            Loan.return_date,
            Loan.status,
        )
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .all()
    )


def get_user_loans(db: Session, user_id: int):
    return (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .filter(User.id == user_id)
        .all()
    )


def get_device_loans(db: Session, device_id: int):
    return (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .filter(Device.id == device_id)
        .all()
    )