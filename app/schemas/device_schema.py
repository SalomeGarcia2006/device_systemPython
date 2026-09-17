from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: bool = True


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: bool


class DeviceUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=1, max_length=100)
    device_type: Optional[str] = Field(None, min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)