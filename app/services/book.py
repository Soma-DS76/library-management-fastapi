from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.borrow import Borrow
from app.models.category import Category
from app.schemas.book import BookCreate, BookUpdate


def create_book(db: Session, data: BookCreate):

    existing_book = db.query(Book).filter( Book.isbn == data.isbn ).first()

    if existing_book:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='ISBN already exists' )

    category = db.query(Category).filter( Category.id == data.category_id ).first()

    if not category:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    if data.available_copies > data.total_copies:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Available copies cannot exceed total copies' )

    book = Book( title=data.title, author=data.author, isbn=data.isbn,
                 category_id=data.category_id, total_copies=data.total_copies,
                 available_copies=data.available_copies, published_year=data.published_year )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_books( db: Session, skip: int, limit: int, 
               title: str | None = None, author: str | None = None, 
               category_id: int | None = None ):

    query = db.query(Book)

    if title:
        query = query.filter( Book.title.ilike(f'%{title}%') )

    if author:
        query = query.filter( Book.author.ilike(f'%{author}%') )

    if category_id is not None:
        query = query.filter( Book.category_id == category_id )

    books = query.offset(skip).limit(limit).all()

    return books


def get_book(db: Session, book_id: int):

    book = db.query(Book).filter( Book.id == book_id ).first()

    if not book:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Book not found' )

    return book


def update_book(db: Session, book_id: int, data: BookUpdate ):

    book = get_book(db, book_id)

    if data.isbn is not None:

        existing_book = db.query(Book).filter( Book.isbn == data.isbn, Book.id != book_id ).first()

        if existing_book:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='ISBN already exists' )

    if data.category_id is not None:

        category = db.query(Category).filter( Category.id == data.category_id ).first()

        if not category:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    new_total = ( data.total_copies if data.total_copies is not None else book.total_copies )

    new_available = ( data.available_copies if data.available_copies is not None 
                      else book.available_copies )

    if new_available > new_total:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Available copies cannot exceed total copies' )

    update_data = data.model_dump( exclude_unset=True )

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book


def delete_book(db: Session, book_id: int):

    book = get_book(db, book_id)

    active_borrow = db.query(Borrow).filter( Borrow.book_id == book_id, 
                                             Borrow.status.in_(['Borrowed', 'Overdue']) ).first()

    if active_borrow:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, 
                             detail='Book cannot be deleted because it is currently borrowed')

    db.delete(book)
    db.commit()

    return { 'message': 'Book deleted successfully' }