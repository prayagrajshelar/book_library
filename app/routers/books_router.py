# app/routers/books_router.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, auth, database, utils

# Add http_bearer at router level so Swagger displays Authorization header
router = APIRouter(
    prefix="/api/v1/books",
    tags=["books"],
    dependencies=[Depends(auth.http_bearer)]
)


@router.post("", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: schemas.BookCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ensure author exists
    author = db.query(models.Author).filter(models.Author.id == book_in.author_id).first()
    utils.assert_resource_found(author, "Author")
    book = models.Book(
        title=book_in.title,
        description=book_in.description,
        publication_date=book_in.publication_date,
        author_id=book_in.author_id,
        available=True
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("", response_model=List[schemas.BookOut])
def list_books(
    skip: int = 0,
    limit: int = 20,
    title: Optional[str] = Query(None),
    author_name: Optional[str] = Query(None),
    available: Optional[bool] = Query(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.Book)
    if title:
        q = q.filter(models.Book.title.ilike(f"%{title}%"))
    if available is not None:
        q = q.filter(models.Book.available == available)
    if author_name:
        q = q.join(models.Author).filter(models.Author.name.ilike(f"%{author_name}%"))
    books = q.offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(
    book_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    utils.assert_resource_found(book, "Book")
    return book


@router.patch("/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_in: schemas.BookUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    utils.assert_resource_found(book, "Book")
    update_data = book_in.dict(exclude_unset=True)
    # if author_id provided, check author exists
    if "author_id" in update_data:
        author = db.query(models.Author).filter(models.Author.id == update_data["author_id"]).first()
        utils.assert_resource_found(author, "Author")
    for key, value in update_data.items():
        setattr(book, key, value)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    utils.assert_resource_found(book, "Book")
    db.delete(book)
    db.commit()
    return {}
