from typing import List, Any

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db

from schemas import ShowBlog, Blog

blog_router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@blog_router.get('/', response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    """Get All Blogs"""
    blogs = db.query(models.Blog).all()
    return blogs


@blog_router.get('/{id}', status_code=200, response_model=ShowBlog)
async def single_blog(id: int, db: Session = Depends(get_db)) -> Any:
    """Get Single Blog"""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


@blog_router.post('/', status_code=status.HTTP_201_CREATED)
async def create(request: Blog, db: Session = Depends(get_db)) -> Any:
    """Create Blog"""
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@blog_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    """Delete Particular Blog"""
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.commit()
    return "Deleted"


@blog_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, request: Blog, db: Session = Depends(get_db)) -> Any:
    """Update Particular Blog"""
    blog = db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body": request.body},
                                                                     synchronize_session="evaluate")
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.commit()
    return blog



