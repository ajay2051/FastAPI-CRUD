from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import Login

login_router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


@login_router.post("/")
async def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    # if not verify_password(user.password, request.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Password Incorrect")
    return user
