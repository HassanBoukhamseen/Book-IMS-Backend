from sqlalchemy import Column, String, Integer, Text, Numeric
from app.database.schemas.base import Base

class Book(Base):
    __tablename__ = 'books'
    book_id = Column("book_id", String(10), primary_key=True)
    title = Column("title", String(350))
    author_name = Column("author_name", Text)
    subtitle = Column("subtitle", String(350))
    thumbnail = Column("thumbnail", String(300))
    genre = Column("genre", String(100))
    description = Column("description", Text)
    year = Column("year", Integer)
    rating = Column("rating", Numeric)
    num_pages = Column("num_pages", Numeric)
    ratings_count = Column("ratings_count", Numeric)
    