# app/routers/authors_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth, database, utils
from ..auth import get_current_user

router = APIRouter(
    prefix="/api/v1/authors",
    tags=["authors"],
    dependencies=[Depends(auth.http_bearer)]
)
@router.post("/", response_model=schemas.AuthorOut)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_author = models.Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=list[schemas.AuthorOut])
def list_authors(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    authors = db.query(models.Author).all()
    return authors


@router.get("/{author_id}", response_model=schemas.AuthorOut)
def get_author(
    author_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

