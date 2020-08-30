import pg8000
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(f'{os.environ["SQLALCHEMY_DATABASE_URI"]}')

def create_db_session(engine = engine):
    session = sessionmaker(bind=engine)
    s = session()
    return s
