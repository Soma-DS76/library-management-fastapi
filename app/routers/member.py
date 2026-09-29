from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.member import ( MemberCreate, MemberResponse, MemberUpdate )
from app.services.member import ( create_member, delete_member,get_member, get_members, update_member )

router = APIRouter( prefix='/members', tags=['Members'] )

@router.post( '', response_model=MemberResponse, status_code=status.HTTP_201_CREATED )
def add_member( data: MemberCreate, db: Session = Depends(get_db) ):
    return create_member(db, data)


@router.get( '', response_model=list[MemberResponse], status_code=status.HTTP_200_OK )
def list_members( skip: int = Query(default=0, ge=0), limit: int = Query(default=10, ge=1, le=100), 
                  db: Session = Depends(get_db) ):
    return get_members( db, skip, limit )


@router.get( '/{member_id}', response_model=MemberResponse, status_code=status.HTTP_200_OK )
def get_member_by_id( member_id: int, db: Session = Depends(get_db) ):
    return get_member( db, member_id )


@router.put( '/{member_id}', response_model=MemberResponse, status_code=status.HTTP_200_OK )
def edit_member( member_id: int, data: MemberUpdate, db: Session = Depends(get_db) ):
    return update_member( db, member_id, data )


@router.delete( '/{member_id}', status_code=status.HTTP_200_OK )
def remove_member( member_id: int, db: Session = Depends(get_db) ):
    return delete_member( db, member_id )