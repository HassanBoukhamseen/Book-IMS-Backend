from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.schemas.base import Base

class BookAuthor(Base):
    __tablename__ = 'books_and_authors'
    book_id =  Column('book_id', String(10), ForeignKey('books.book_id'))
    author_id = Column('author_id', Integer, ForeignKey('authors.author_id'))
    __table_args__ = (
        PrimaryKeyConstraint('book_id', 'author_id'),
    )