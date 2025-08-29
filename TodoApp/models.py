from database import Base
from sqlalchemy import Column, Integer, String, Boolean


# This create table in the database
class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    complete = Column(Boolean, index=True, default=False)
    