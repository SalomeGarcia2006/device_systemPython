from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.loan_schema import (
    LoanCreate,
    LoanDetailResponse,
    LoanResponse,
)
from app.services.loan_service import (
    create_loan,
    get_loan,
    get_loan_details,
    get_loans,
    return_loan,
)

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene los préstamos con filtros opcionales.",
)
def list_loans(
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Filtrar por estado del préstamo",
    ),
    user_email: Optional[str] = Query(
        None,
        description="Filtrar por correo del usuario",
    ),
    device_type: Optional[str] = Query(
        None,
        description="Filtrar por tipo de dispositivo",
    ),
    db: Session = Depends(get_db),
):
    return get_loans(
        db,
        status=status_filter,
        user_email=user_email,
        device_type=device_type,
    )


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Consultar detalles de préstamos",
    description="Obtiene información del préstamo, usuario y dispositivo mediante JOIN.",
)
def loan_details(
    db: Session = Depends(get_db),
):
    return get_loan_details(db)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo",
)
def get_loan_by_id(
    loan_id: int,
    db: Session = Depends(get_db),
):
    loan = get_loan(db, loan_id)

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado",
        )

    return loan


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea un préstamo y cambia el dispositivo a no disponible.",
)
def create_loan_route(
    data: LoanCreate,
    db: Session = Depends(get_db),
):
    loan = create_loan(db, data)

    if loan == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    if loan == "device_not_found":
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado",
        )

    if loan == "device_unavailable":
        raise HTTPException(
            status_code=409,
            detail="El dispositivo no está disponible",
        )

    return loan


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver préstamo",
    description="Registra la devolución y vuelve a marcar el dispositivo como disponible.",
)
def return_loan_route(
    loan_id: int,
    db: Session = Depends(get_db),
):
    loan = return_loan(db, loan_id)

    if loan == "loan_not_found":
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado",
        )

    if loan == "already_returned":
        raise HTTPException(
            status_code=409,
            detail="El préstamo ya fue devuelto",
        )

    return loan