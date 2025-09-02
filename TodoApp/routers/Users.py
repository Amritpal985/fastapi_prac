from fastapi import APIRouter, Body,Path, Query, HTTPException, Depends, status
from models import Todos, Users
from database import  Sessionlocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from .auth import get_current_user

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UpdatedPasswordrequest(BaseModel):
    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)

class UpdatedPhonerequest(BaseModel):
    new_phone: str = Field(min_length=10,max_length=10)    


# get_user
@router.get("/get_info",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        todo_model = db.query(Users).filter(Users.id == user.get('id')).all()
        return todo_model 
    except:
        raise HTTPException(status_code=404,detail='Something went wrong')

# change password
@router.put('/update_password/',status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,db:db_dependency,request: UpdatedPasswordrequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="User not found")
        if not bcrypt_context.verify(request.old_password,user_model.hashed_password):
            raise HTTPException(status_code=400,detail="Old password does not match")
        user_model.hashed_password = bcrypt_context.hash(request.new_password)
        db.add(user_model)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback() 
        raise HTTPException(status_code=404,detail= f"Something went wrong {e}")
    
# update phone number
@router.put('/update_phone/',status_code=status.HTTP_204_NO_CONTENT)
async def update_phone(user:user_dependency,db:db_dependency,request: UpdatedPhonerequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid user")
    try:
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="User not found")
        user_model.phone_number = request.new_phone
        db.add(user_model)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback() 
        raise HTTPException(status_code=404,detail= f"Something went wrong {e}")