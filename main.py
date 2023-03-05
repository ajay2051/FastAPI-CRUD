import uvicorn
from fastapi import FastAPI

import models
from blog.routers.authentication import login_router
from blog.routers import blog_router, user_router
from database import engine


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(login_router)
app.include_router(blog_router)
app.include_router(user_router)


# Run Project At Specified Port
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
