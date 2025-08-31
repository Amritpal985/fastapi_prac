from fastapi import APIRouter, Body,Path, Query, HTTPException, Depends, status
from models import Todos
from database import  Sessionlocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter()

# Dependency injection for database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=5)
    description:str = Field(min_length=5,max_length=90)
    priority:int = Field(gt=0,lt=6)
    complete:bool = False 



@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()

# Fetch Single Todo 
@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db: db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    todo_model =  db.query(Todos).filter(Todos.id==todo_id,Todos.owner_id==user.get("id")).first()
    if todo_model is not None:
        return todo_model 
    raise HTTPException(status_code=404,detail="Todo is doesnot exists")

# create a new todo
@router.post("/todo/create_todo",response_model=TodoRequest,status_code=status.HTTP_201_CREATED)
async def create_new_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        new_todo = Todos(**todo_request.dict(),owner_id=user.get("id"))
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except SQLAlchemyError:
        raise HTTPException(status_code=400,detail="Something went wrong")

@router.put("/todo/{todo_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
        if todo_model is  None:
            raise HTTPException(status_code=404,detail='Todo not found')
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db.commit()
        db.refresh(todo_model)
        return 
    except SQLAlchemyError:
        raise HTTPException(status_code=400,detail="Something went wrong")
    
# delete todo
@router.delete("/todo/delete_todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id == user.get('id')).first()
        if todo_model is None:
            raise HTTPException(status_code=404,detail="Todo not found")
        db.delete(todo_model)
        db.commit()
        return 
    except SQLAlchemyError:
        raise HTTPException(status_code=400,detail="Something went wrong")
        

