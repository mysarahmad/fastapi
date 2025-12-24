from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from passlib.context import CryptContext
from database import SessionLocal



class User(Base):
    __tablename__= "userinfo"
    id = Column(Integer,primary_key=True,index=True)
    name  = Column(String)
    email = Column(String)
    password = Column(String)
   

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

