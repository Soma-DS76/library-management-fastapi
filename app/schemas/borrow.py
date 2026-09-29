from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BorrowCreate(BaseModel):

    book_id: int = Field( gt=0 )
    member_id: int = Field( gt=0 )
    borrow_date: date

class ReturnBook(BaseModel):
    return_date: date
    
class BorrowResponse(BaseModel):

    id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str
    model_config = ConfigDict(from_attributes=True)