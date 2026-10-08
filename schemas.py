from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator, ConfigDict


class StudentBase(BaseModel):
    student_id: str
    name: str
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    @field_validator("name", "student_id")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()


class StudentCreate(StudentBase):
    @model_validator(mode="after")
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError("at least one of email or phone must be provided")
        return self


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentOut(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
