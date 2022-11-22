import os
from fastapi import FastAPI,status
from models import Blog,Author
from redis_om.model import NotFoundError
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()

def format_response(data):
    return [dat.dict() for dat in data]

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

@app.get("/authors/{pk}")
async def get_author(pk: str):
    try:
        author = Author.get(pk)
    except NotFoundError:
        return {"mesage":"Author not found"}  

    return author 


@app.get("/blogs/{pk}")
async def get_blog(pk: str):
    try:
        blog = Blog.get(pk)
    except NotFoundError:
        return {"mesage":"Blog not found"}  

    return blog

@app.put("/blogs/{pk}")
async def update_blog(pk:str,body:dict):
    try:
        blog = Blog.get(pk)
    except NotFoundError:
        return {"message":"Blog not found"}    

    blog.title = body["title"]
    blog.content = body["content"]

    blog.save()

    return blog

@app.delete("/blogs/{pk}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(pk:str):
    Blog.delete(pk)

    return {"message":"record deleted successfully"}


@app.post("/blogs/find")
async def find_blog_by_name(title: str ):
    response = Blog.find(Blog.title == title).all()

    return format_response(response)


@app.post("/blogs/find/authors")
async def find_blog_by_author(firstname: str ):
    response = Blog.find(Blog.author.firstname == firstname).all()

    return format_response(response)


