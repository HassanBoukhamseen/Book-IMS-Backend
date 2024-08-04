from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    book_id: str
    title: str
    subtitle: str
    thumbnail: str
    author_id: int
    author_name: int
    genre: str
    description: str
    year: int
    rating: float
    num_pages: int
    ratings_count: int

class BookUpdateCurrent(BaseModel):
    book_id: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    thumbnail: Optional[str] = None
    author_id: Optional[int] = None
    author_name: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    num_pages: Optional[int] = None
    ratings_count: Optional[int] = None