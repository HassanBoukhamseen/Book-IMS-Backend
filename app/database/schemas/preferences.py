from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.schemas.base import Base

class Preferences(Base):
    __tablename__ = 'preferences'
    email = Column("email", String(100), ForeignKey('users.email'), primary_key=True)
    preference = Column("preference", String(30), primary_key=True)
    user = relationship("User")