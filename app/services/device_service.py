from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DeviceUpdatePartial,
)


def get_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
):
    query = db.query(Device)

    filters = []

    if device_type:
        filters.append(Device.device_type.ilike(f"%{device_type}%"))

    if is_available is not None:
        filters.append(Device.is_available == is_available)

    if brand:
        filters.append(Device.brand.ilike(f"%{brand}%"))

    if search:
        filters.append(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.device_type.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%"),
            )
        )

    if filters:
        query = query.filter(and_(*filters))

    return query.all()


def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()


def create_device(db: Session, data: DeviceCreate):
    existing_device = (
        db.query(Device)
        .filter(Device.serial_number == data.serial_number)
        .first()
    )

    if existing_device:
        return None

    device = Device(
        name=data.name,
        serial_number=data.serial_number,
        device_type=data.device_type,
        brand=data.brand,
        is_available=data.is_available,
    )

    db.add(device)

    try:
        db.commit()
        db.refresh(device)
    except IntegrityError:
        db.rollback()
        return None

    return device


def update_device(db: Session, device_id: int, data: DeviceUpdate):
    device = get_device(db, device_id)

    if not device:
        return None

    duplicate = (
        db.query(Device)
        .filter(
            Device.serial_number == data.serial_number,
            Device.id != device_id,
        )
        .first()
    )

    if duplicate:
        return "duplicate"

    device.name = data.name
    device.serial_number = data.serial_number
    device.device_type = data.device_type
    device.brand = data.brand
    device.is_available = data.is_available

    try:
        db.commit()
        db.refresh(device)
    except IntegrityError:
        db.rollback()
        return "duplicate"

    return device


def update_device_partial(
    db: Session,
    device_id: int,
    data: DeviceUpdatePartial,
):
    device = get_device(db, device_id)

    if not device:
        return None

    update_data = data.model_dump(exclude_unset=True)

    if "serial_number" in update_data:
        duplicate = (
            db.query(Device)
            .filter(
                Device.serial_number == update_data["serial_number"],
                Device.id != device_id,
            )
            .first()
        )

        if duplicate:
            return "duplicate"

    for field, value in update_data.items():
        setattr(device, field, value)

    try:
        db.commit()
        db.refresh(device)
    except IntegrityError:
        db.rollback()
        return "duplicate"

    return device


def delete_device(db: Session, device_id: int):
    device = get_device(db, device_id)

    if not device:
        return None

    db.delete(device)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return "conflict"

    return device