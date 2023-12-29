from fastapi import (
    FastAPI,
    HTTPException,
    status,
)
from pydantic import BaseModel
from typing import Optional
from random import randrange

import uvicorn

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None


# Define dummy data
my_list = [
    {
        'title': 'title1',
        'content': 'content1',
        'id': 1,
    },
    {
        'title': 'title2',
        'content': 'content2',
        'id': 2,
    },
]


# Implement home-page endpoint
@app.get('/')
def home():
    return 'Hello World!'


# Implement 'get all posts' endpoint
@app.get('/posts')
def get_all_posts():
    return {'data': my_list}


# Implement 'create post' endpoint
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    my_list.append(post_dict)
    return {'data': post_dict}


# Implement 'get latest post' endpoint
@app.get('/posts/latest')
def get_latest_post():
    post = my_list[-1]
    return {'post_detail': post}


# Implement 'get post by ID' endpoint
@app.get('/posts/{id}')
def get_post_by_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with ID {id} not found',
        )
    return {'post_detail': post}


# Implement 'delete post' endpoint
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with ID {id} does not exist',
        )
    my_list.pop(post_index)
    return {'message': f'Post with ID {id} successfully deleted'}


# Implement 'update post' endpoint
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with ID {id} does not exist',
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_list[post_index] = post_dict
    return {'message': f'Post with ID {id} successfully updated'}


# Helper functions
def find_post(id):
    for p in my_list:
        if p['id'] == id:
            return p


def find_index_post(id):
    for idx, p in enumerate(my_list):
        if p['id'] == id:
            return idx


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
