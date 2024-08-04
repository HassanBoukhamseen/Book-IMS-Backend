from sqlalchemy import Column, Text, Integer, String
from app.database.schemas.base import Base

class MessageHistory(Base):
    __tablename__ = 'message_history'
    id =  Column('id', Integer, primary_key=True, autoincrement=True)
    messages = Column('messages', Text)
    role = Column('role', String(7))