from sqlalchemy.orm import declarative_base
from app.database.connector import connect_to_db

engine, session = connect_to_db()
Base = declarative_base()

