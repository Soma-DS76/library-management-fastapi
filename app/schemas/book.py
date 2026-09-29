from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):

    title: str = Field( min_length=1, max_length=200 )
    author: str = Field( min_length=1, max_length=150 )
    isbn: str = Field( min_length=10, max_length=20 )
    category_id: int = Field( gt=0 )
    total_copies: int = Field( gt=0 )
    available_copies: int = Field( ge=0 )
    published_year: Optional[int] = Field( default=None, ge=1000, le=2100 )


class BookUpdate(BaseModel):

    title: Optional[str] = Field( default=None, min_length=1, max_length=200 )
    author: Optional[str] = Field( default=None, min_length=1, max_length=150 )
    isbn: Optional[str] = Field( default=None, min_length=10, max_length=20 )
    category_id: Optional[int] = Field( default=None, gt=0 )
    total_copies: Optional[int] = Field( default=None, gt=0 )
    available_copies: Optional[int] = Field( default=None, ge=0 )
    published_year: Optional[int] = Field( default=None, ge=1000, le=2100 )


class BookResponse(BaseModel):

    id: int
    title:  str
    author: str
    isbn: str
    category_id: int
    total_copies: int
    available_copies: int
    published_year: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)