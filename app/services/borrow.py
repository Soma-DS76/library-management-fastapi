from datetime import date, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.borrow import Borrow
from app.models.member import Member
from app.schemas.borrow import BorrowCreate, ReturnBook


def borrow_book( db: Session, data: BorrowCreate ):

    book = db.query(Book).filter( Book.id == data.book_id ).first()

    if not book:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Book not found' )

    member = db.query(Member).filter( Member.id == data.member_id ).first()

    if not member:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Member not found' )

    if not member.is_active:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive member cannot borrow books')

    if book.available_copies <= 0:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Book is not available' )

    active_borrows = db.query(Borrow).filter( Borrow.member_id == data.member_id, 
                                              Borrow.status.in_(['Borrowed', 'Overdue'])).count()

    if active_borrows >= 3:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Member cannot borrow more than 3 books' )

    existing_borrow = db.query(Borrow).filter( Borrow.member_id == data.member_id,
                                               Borrow.book_id == data.book_id, Borrow.status.in_(['Borrowed', 'Overdue']) ).first()

    if existing_borrow:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Member already borrowed this book')

    due_date = data.borrow_date + timedelta( days=14 )

    borrow = Borrow( book_id=data.book_id,member_id=data.member_id,
                     borrow_date=data.borrow_date,due_date=due_date,return_date=None,status='Borrowed' )

    book.available_copies -= 1

    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return borrow


def return_book( db: Session, borrow_id: int, data: ReturnBook ):

    borrow = db.query(Borrow).filter( Borrow.id == borrow_id ).first()

    if not borrow:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Borrow record not found' )

    if borrow.return_date is not None:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Book has already been returned' )

    if data.return_date < borrow.borrow_date:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Return date cannot be before borrow date' )

    book = db.query(Book).filter( Book.id == borrow.book_id ).first()

    if not book:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Book not found' )

    borrow.return_date = data.return_date
    borrow.status = 'Returned'

    if book.available_copies < book.total_copies:
        book.available_copies += 1

    db.commit()
    db.refresh(borrow)

    return borrow


def get_member_books( db: Session, member_id: int ):

    member = db.query(Member).filter( Member.id == member_id ).first()

    if not member:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Member not found' )

    borrows = db.query(Borrow).filter( Borrow.member_id == member_id, Borrow.status.in_(['Borrowed', 'Overdue']),
                                      Borrow.return_date.is_(None) ).all()

    return borrows


def get_book_history( db: Session, book_id: int ):

    book = db.query(Book).filter( Book.id == book_id ).first()

    if not book:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Book not found' )

    history = db.query(Borrow).filter( Borrow.book_id == book_id ).order_by( Borrow.borrow_date.desc() ).all()

    return history


def get_overdue_books(db: Session):

    today = date.today()
    overdue_records = db.query(Borrow).filter( Borrow.due_date < today, Borrow.return_date.is_(None),
                                               Borrow.status.in_(['Borrowed', 'Overdue']) ).all()
    for borrow in overdue_records:
        if borrow.status != 'Overdue':
            borrow.status = 'Overdue'

    db.commit()
    return overdue_records