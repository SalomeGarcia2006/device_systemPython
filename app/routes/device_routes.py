from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.user_dependencies import (
    get_current_active_user,
    require_admin,
    require_admin_or_support,
)
from app.schemas.device_schema import DeviceCreate, DeviceResponse, DeviceUpdate, DeviceUpdatePartial
from app.schemas.loan_schema import LoanResponse
from app.services.device_service import create_device, delete_device, get_device, get_devices, update_device, update_device_partial
from app.services.loan_service import get_device_loans


router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/", response_model=list[DeviceResponse], summary="Listar dispositivos")
def list_devices(
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return get_devices(db, device_type=device_type, is_available=is_available, brand=brand, search=search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo")
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, summary="Crear dispositivo")
def create_device_route(data: DeviceCreate, db: Session = Depends(get_db), current_user=Depends(require_admin_or_support)):
    device = create_device(db, data)
    if device is None:
        raise HTTPException(status_code=409, detail="El número de serie ya existe")
    return device


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo")
def update_device_route(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db), current_user=Depends(require_admin_or_support)):
    device = update_device(db, device_id, data)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if device == "duplicate":
        raise HTTPException(status_code=409, detail="El número de serie ya existe")
    return device


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar parcialmente un dispositivo")
def update_device_partial_route(device_id: int, data: DeviceUpdatePartial, db: Session = Depends(get_db), current_user=Depends(require_admin_or_support)):
    device = update_device_partial(db, device_id, data)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if device == "duplicate":
        raise HTTPException(status_code=409, detail="El número de serie ya existe")
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar dispositivo")
def delete_device_route(device_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    result = delete_device(db, device_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if result == "conflict":
        raise HTTPException(status_code=409, detail="No se puede eliminar el dispositivo porque tiene préstamos asociados")
    return None


@router.get("/{device_id}/loans", response_model=list[LoanResponse], summary="Consultar préstamos de un dispositivo")
def device_loans(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    device = get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return get_device_loans(db, device_id)