from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class MemberCreate(BaseModel):

    name: str = Field( min_length=2, max_length=100 )
    email: EmailStr
    phone: str = Field( min_length=10, max_length=15 )
    address: str = Field( min_length=2, max_length=255 )

    membership_date: date
    is_active: bool = True

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        phone = value.strip()

        if phone.startswith('+'):
            number = phone[1:]
        else:
            number = phone

        if not number.isdigit():
            raise ValueError( 'Phone number must contain only digits' )

        if len(number) < 10 or len(number) > 15:
            raise ValueError( 'Phone number must contain 10 to 15 digits' )

        return phone


class MemberUpdate(BaseModel):

    name: Optional[str] = Field( default=None, min_length=2, max_length=100 )
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field( default=None, min_length=10, max_length=15 )
    address: Optional[str] = Field( default=None, min_length=2, max_length=255 )
    membership_date: Optional[date] = None
    is_active: Optional[bool] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        phone = value.strip()

        if phone.startswith('+'):
            number = phone[1:]
        else:
            number = phone

        if not number.isdigit():
            raise ValueError( 'Phone number must contain only digits' )

        if len(number) < 10 or len(number) > 15:
            raise ValueError( 'Phone number must contain 10 to 15 digits' )

        return phone


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str
    membership_date: date
    is_active: bool
    model_config = ConfigDict(from_attributes=True)