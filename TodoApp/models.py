from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey



# users class
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    username = Column(String,unique=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)

# This create table in the database
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    complete = Column(Boolean, index=True, default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))
    