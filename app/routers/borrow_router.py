# app/routers/borrow_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth, database, utils
from datetime import datetime

# Add http_bearer dependency so Swagger shows Authorization header field
router = APIRouter(prefix="/api/v1", tags=["borrow"], dependencies=[Depends(auth.http_bearer)])


@router.post("/borrow", response_model=schemas.BorrowRecordOut)
def borrow_book(
    payload: schemas.BorrowCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    book = db.query(models.Book).filter(models.Book.id == payload.book_id).first()
    utils.assert_resource_found(book, "Book")
    if not book.available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is currently not available")
    # Create record and mark book unavailable
    record = models.BorrowRecord(user_id=current_user.id, book_id=book.id)
    book.available = False
    db.add(record)
    db.add(book)
    db.commit()
    db.refresh(record)
    return record


@router.post("/return/{record_id}", response_model=schemas.BorrowRecordOut)
def return_book(
    record_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    record = db.query(models.BorrowRecord).filter(models.BorrowRecord.id == record_id).first()
    utils.assert_resource_found(record, "Borrow record")
    if record.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")
    if record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to return this record")
    record.return_date = datetime.utcnow()
    # set book available
    book = db.query(models.Book).filter(models.Book.id == record.book_id).first()
    if book:
        book.available = True
        db.add(book)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/borrow/history", response_model=List[schemas.BorrowRecordOut])
def borrow_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # return only user's history
    records = db.query(models.BorrowRecord).filter(models.BorrowRecord.user_id == current_user.id).order_by(models.BorrowRecord.borrow_date.desc()).offset(skip).limit(limit).all()
    return records
