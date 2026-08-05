import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

engine = create_engine(os.getenv('DB_URL'))

session = sessionmaker(autocommit = False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



