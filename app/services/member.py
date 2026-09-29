from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.borrow import Borrow
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


def create_member(db: Session, data: MemberCreate):

    existing_member = db.query(Member).filter( Member.email == data.email ).first()
    if existing_member:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Email already exists' )

    member = Member( name=data.name, email=data.email, phone=data.phone, address=data.address,
                     membership_date=data.membership_date, is_active=data.is_active )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_members( db: Session, skip: int, limit: int ):

    members = db.query(Member).offset( skip ).limit( limit ).all()
    return members


def get_member( db: Session, member_id: int ):

    member = db.query(Member).filter( Member.id == member_id ).first()
    if not member:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Member not found' )

    return member


def update_member( db: Session, member_id: int, data: MemberUpdate ):

    member = get_member(db, member_id)
    if data.email is not None:
        existing_member = db.query(Member).filter( Member.email == data.email, Member.id != member_id ).first()

        if existing_member:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail='Email already exists' )

    update_data = data.model_dump( exclude_unset=True )

    for field, value in update_data.items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)

    return member


def delete_member( db: Session, member_id: int ):

    member = get_member(db, member_id)
    active_borrow = db.query(Borrow).filter( Borrow.member_id == member_id, 
                                             Borrow.status.in_(['Borrowed', 'Overdue']) ).first()
    if active_borrow:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, 
                             detail='Member cannot be deleted because books are still borrowed' )

    db.delete(member)
    db.commit()

    return { 'message': 'Member deleted successfully' }