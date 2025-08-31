from fastapi import APIRouter, Body,Path, Query, HTTPException, Depends, status
from models import Todos
from database import  Sessionlocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# Dependency injection for database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    if user.get("role") != "admin":
        raise HTTPException(status_code=403,detail="Not authorized to perform requested action")
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    if user.get("role") != "admin":
        raise HTTPException(status_code=403,detail="Not authorized to perform requested action")
    try:
        todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
        if todo_model is None:
            raise HTTPException(status_code=404,detail="Todo not found")
        db.delete(todo_model)
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=400,detail="Something went wrong")

