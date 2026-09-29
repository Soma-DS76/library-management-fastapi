from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.borrow import ( BorrowCreate, BorrowResponse, ReturnBook )
from app.services.borrow import ( borrow_book, get_book_history, 
                                  get_member_books, get_overdue_books, return_book )


router = APIRouter( tags=['Borrow and Return'] )

@router.post( '/borrow', response_model=BorrowResponse, status_code=status.HTTP_201_CREATED )
def borrow( data: BorrowCreate, db: Session = Depends(get_db) ):
    return borrow_book( db, data )


@router.put( '/return/{borrow_id}', response_model=BorrowResponse, status_code=status.HTTP_200_OK )
def return_borrowed_book( borrow_id: int, data: ReturnBook, db: Session = Depends(get_db) ):
    return return_book( db, borrow_id, data )


@router.get( '/members/{member_id}/books', response_model=list[BorrowResponse], 
              status_code=status.HTTP_200_OK )
def member_books( member_id: int, db: Session = Depends(get_db)):
    return get_member_books( db, member_id )


@router.get( '/books/{book_id}/borrow-history', response_model=list[BorrowResponse], 
              status_code=status.HTTP_200_OK )
def book_borrow_history( book_id: int, db: Session = Depends(get_db)):
    return get_book_history( db, book_id )


@router.get( '/borrow/overdue', response_model=list[BorrowResponse], status_code=status.HTTP_200_OK )
def overdue_books( db: Session = Depends(get_db)):
    return get_overdue_books(db)