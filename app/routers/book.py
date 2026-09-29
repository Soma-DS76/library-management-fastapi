from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import ( BookCreate,BookResponse, BookUpdate )
from app.services.book import ( create_book,delete_book, get_book,get_books,update_book )


router = APIRouter( prefix='/books', tags=['Books'] )

@router.post( '', response_model=BookResponse, status_code=status.HTTP_201_CREATED )
def add_book( data: BookCreate, db: Session = Depends(get_db)  ):
    return create_book(db, data)


@router.get( '', response_model=list[BookResponse], status_code=status.HTTP_200_OK )
def list_books( title: Optional[str] = Query(default=None),author: Optional[str] = Query(default=None),
                category_id: Optional[int] = Query(default=None, gt=0),skip: int = Query(default=0, ge=0),
                limit: int = Query(default=10, ge=1, le=100),db: Session = Depends(get_db)):
    
    return get_books( db, skip, limit, title, author, category_id )


@router.get( '/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK )
def get_book_by_id( book_id: int, db: Session = Depends(get_db) ):
    return get_book(db, book_id)


@router.put( '/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK )
def edit_book( book_id: int, data: BookUpdate, db: Session = Depends(get_db) ):
    return update_book( db, book_id, data )


@router.delete( '/{book_id}', status_code=status.HTTP_200_OK )
def remove_book( book_id: int, db: Session = Depends(get_db) ):
    return delete_book( db, book_id )