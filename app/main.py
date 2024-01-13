from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='postgres', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was succesfull')
except Exception as error:
    print('Connection too database failed')
    print("Érror: ", error)


my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1},
            {"title": "favorite food", "content":"I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id: int):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!"}

# getting all posts
@app.get("/posts")
def get_posts():
    return{"data": my_posts}

# creating a post
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict=(post.dict())
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{"data": post_dict} 

# getting individual post by id
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return('message': f"post with id :{id} was not found")
    return{"post_detail": post}

# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index of post id
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    # pop the id
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating a post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post:Post):
    # find index of post id
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
     