from app.database.database import Base
from sqlalchemy import Column, Integer,String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key= True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)