from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.database import get_db
from app.dependencies.user_dependencies import (
    get_current_active_user,
    require_admin_or_support,
)
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse
from app.services.loan_service import create_loan, get_loan, get_loan_details, get_loans, return_loan


router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("/", response_model=list[LoanResponse], summary="Listar préstamos")
def list_loans(
    status_filter: Optional[str] = Query(None, alias="status"),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return get_loans(db, status=status_filter, user_email=user_email, device_type=device_type)


@router.get("/details", response_model=list[LoanDetailResponse], summary="Consultar detalles de préstamos")
def loan_details(db: Session = Depends(get_db), current_user=Depends(require_admin_or_support)):
    return get_loan_details(db)


@router.get("/{loan_id}", response_model=LoanResponse, summary="Obtener préstamo")
def get_loan_by_id(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    loan = get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Crear préstamo")
@limiter.limit("10/minute")
def create_loan_route(request: Request, data: LoanCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    if current_user.role == "user" and data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes crear préstamos para tu propio usuario",
        )
    loan = create_loan(db, data)
    if loan == "user_not_found":
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if loan == "user_inactive":
        raise HTTPException(status_code=403, detail="El usuario del préstamo está inactivo")
    if loan == "device_not_found":
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if loan == "device_unavailable":
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")
    return loan


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver préstamo")
def return_loan_route(loan_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin_or_support)):
    loan = return_loan(db, loan_id)
    if loan == "loan_not_found":
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if loan == "already_returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")
    return loan