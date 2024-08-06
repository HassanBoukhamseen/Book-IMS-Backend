from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from app.database.schemas.base import Base

class LikedBooks(Base):
    __tablename__ = 'liked_books'
    email = Column('email', String(100), ForeignKey('users.email'))
    book_id =  Column('book_id', String(10), ForeignKey('books.book_id'))
    __table_args__ = (
        PrimaryKeyConstraint('email', 'book_id'),
    )