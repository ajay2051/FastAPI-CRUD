from typing import Any, List

from fastapi import APIRouter, status, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from blog.routers.authentication import password_context

from database import get_db
from schemas import User, ShowUser

user_router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@user_router.post("/", status_code=status.HTTP_201_CREATED, )
async def create_user(request: User, db: Session = Depends(get_db)) -> Any:
    """Create New User"""
    hashed_password = password_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/", response_model=List[ShowUser])
async def all_users(db: Session = Depends(get_db)) -> Any:
    """Get All Users"""
    users = db.query(models.User).all()
    return users


@user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def user(id: int, db: Session = Depends(get_db)) -> Any:
    """Get Particular User"""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
