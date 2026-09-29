from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import ( CategoryCreate, CategoryResponse, CategoryUpdate )
from app.services.category import ( create_category, delete_category, get_categories, update_category )


router = APIRouter( prefix='/categories', tags=['Categories'] )


@router.post( '', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED )
def add_category( data: CategoryCreate, db: Session = Depends(get_db) ):

    return create_category(db, data)


@router.get( '', response_model=list[CategoryResponse], status_code=status.HTTP_200_OK )
def list_categories( skip: int = Query(default=0, ge=0), limit: int = Query(default=10, ge=1, le=100), 
                     db: Session = Depends(get_db) ):
    
    return get_categories(db, skip, limit)


@router.put( '/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK )
def edit_category( category_id: int, data: CategoryUpdate, db: Session = Depends(get_db) ):

    return update_category( db, category_id, data )


@router.delete( '/{category_id}', status_code=status.HTTP_200_OK )
def remove_category( category_id: int, db: Session = Depends(get_db) ):
    
    return delete_category( db, category_id )