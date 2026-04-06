from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date as DateType
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: str
    category: str
    date: DateType
    notes: Optional[str] = None
    owner_id: int


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[DateType] = None
    notes: Optional[str] = None


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: DateType
    notes: Optional[str] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)