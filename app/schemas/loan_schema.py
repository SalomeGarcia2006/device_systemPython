from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    device_id: int
    device_name: str
    serial_number: str
    device_type: str
    loan_date: datetime
    return_date: Optional[datetime]
    status: str