from fastapi import FastAPI
from models import Blog,Author
from redis_om.model import NotFoundError


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"This is the root"}


@app.post("/authors")
async def create_author(body:Author):
    author = Author(
        firstname = body.firstname,
        lastname = body.lastname,
        email = body.email,
        bio = body.bio,
        date_joined = body.date_joined
    )

    author.save()

    return author

@app.post("/blogs")
async def create_blog(body:dict):
    author = Author.get(body["author_id"])
    blog = Blog(
        title = body["title"],
        content = body["content"],
        author = author
    )
    
    blog.save()

    return blog
