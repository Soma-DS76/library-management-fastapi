from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, data: CategoryCreate):

    existing_category = db.query(Category).filter( Category.category_name == data.category_name ).first()

    if existing_category:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, 
                             detail='Category name already exists' )

    category = Category( category_name=data.category_name, description=data.description )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session, skip: int, limit: int):

    categories = db.query(Category).offset(skip).limit(limit).all()

    return categories


def get_category(db: Session, category_id: int):

    category = db.query(Category).filter( Category.id == category_id ).first()

    if not category:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Category not found' )

    return category


def update_category( db: Session, category_id: int, data: CategoryUpdate ):

    category = get_category(db, category_id)

    if data.category_name is not None:

        existing_category = db.query(Category).filter( Category.category_name == data.category_name, 
                                                       Category.id != category_id ).first()

        if existing_category:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, 
                                 detail='Category name already exists' )

        category.category_name = data.category_name

    if data.description is not None:
        category.description = data.description

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int):

    category = get_category(db, category_id)

    if category.books:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, 
                             detail='Category cannot be deleted because it contains books' )

    db.delete(category)
    db.commit()

    return { 'message': 'Category deleted successfully' }