# app/schemas.py  (for Pydantic v2)
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

# --- User schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool


# --- Token schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# --- Author schemas ---
class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    bio: Optional[str]
    created_at: datetime

class AuthorDetail(AuthorOut):
    books: List["BookOut"] = []

# --- Book schemas ---
class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    publication_date: Optional[str] = None
    author_id: int

class BookUpdate(BaseModel):
    # make all fields optional so PATCH accepts partial updates
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str] = None
    description: Optional[str] = None
    publication_date: Optional[str] = None
    author_id: Optional[int] = None
    available: Optional[bool] = None

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    publication_date: Optional[str]
    available: bool
    author_id: Optional[int]
    created_at: datetime

AuthorDetail.model_rebuild()

# --- Borrow schemas ---
class BorrowCreate(BaseModel):
    book_id: int

class BorrowRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
