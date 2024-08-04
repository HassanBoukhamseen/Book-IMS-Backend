from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connect_to_db(username="postgres", password="password", host="127.0.0.1", port="5432", db_name="test"):
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session