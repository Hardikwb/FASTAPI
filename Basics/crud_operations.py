# http://127.0.0.1:8000/redoc#operation/update_post_id_posts_v2_update__id__put
from typing import Union

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
# /items/8255225?q=57

@app.get('/users')
def get_users():
    return [
        {
            "name":"Hitesh",
            "email":"hitesh!hiteshchaidhary.com",
            "contact":"9856985678",
            "courseCount":4,
            "isVerified":True,
        },
        {
            "name":"Mark",
            "email":"mark@example.com",
            "contact":"9658741236",
            "courseCount":2,
            "isVerified":False,
        },
    ]

@app.get('/posts')
def get_posts():
    return {"posts":[{"These are collection 1"},{"These are collection 2"}]}

# If 2 have same path then one at top will execute

@app.post('/createposts')
def create_posts(payload: dict=Body(...)):
    return {
        "message": "Post created successfully",
        "data": payload,
        "new post":f"title: {payload['title']} content:{payload['content']}"
    }

# using pydantic
from pydantic import BaseModel
from typing import Optional
class manage_post_pydantic(BaseModel):
    title:str
    content:str
    post_published:bool=True
    rating:Optional[int]=None

@app.post("/sendcreatedpost")
def send_created_post(post:manage_post_pydantic):
    # print(post)
    #  to get in dictionary form
    print(post.dict())
    return f" title:{post.title} content:{post.content} post_published:{post.post_published} rating:{post.rating} "

my_posts=[{"id":1,"title":"title of post 1","content":"content of post 1"},
          {"id":2,"title":"Favourite Food","content":"I love Pizza"}]

@app.get('/seeposts')
def see_all_post():
    return {"data":my_posts}


from random import randrange
@app.post('/post')
def create_post(post:manage_post_pydantic):
    post_dict=post.dict() 
    post_dict['id']=randrange(0,12563)
    my_posts.append(post_dict)
    return {"data":post_dict}


# from fastapi import Response,status
# @app.get('/posts/{id}')
# def get_id_post(id:int,response:Response):
#     for post in my_posts:
#         if(post['id']==id):
#            return (
#                 f"id: {post['id']} "
#                 f"title: {post['title']} "
#                 f"content: {post['content']} "
#             )
#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {"message": f"Post with id: {id} not found"}

# wAY-2
#  Get individual Post
from fastapi import HTTPException,status,Response
# by defualt 201 code
@app.get('/posts/{id}',status_code=status.HTTP_201_CREATED)
def get_id_post(id:int):
    for post in my_posts:
        if(post['id']==id):
           return (
                f"id: {post['id']} "
                f"title: {post['title']} "
                f"content: {post['content']} "
            ) 
    raise HTTPException(status_code=404, detail="Post not found")

def find_post_by_id(id:int):
    for i in enumerate(my_posts):
        if int(i[1]['id'])==id:
            # return f"title:{i[1]['title']}"
            return i[1]

def find_post_id_index(id:int):
    #  i means 0,1,2.. and p is the the dict
    for i,p in enumerate(my_posts):
        if(p['id']==id):
            return i       

# Delete a post
@app.delete("/posts/{id}")
def delete_post_id(id:int,status_code=status.HTTP_200_OK):
    index = find_post_id_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
    )
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


class UpdatePost(BaseModel):
    new_title: str
    new_content: str

@app.put("/posts/v1/update/{id}")
def update_post_id(id: int, post: UpdatePost):
    index = find_post_id_index(id)
    current_post = my_posts[index]

    current_post["id"] = id
    current_post["title"] = post.new_title
    current_post["content"] = post.new_content

    return f"title: {current_post['title']} content: {current_post['content']}"

from fastapi import Body

@app.put("/posts/v2/update/{id}")
def update_post_id(
    id: int,
    new_title: str = Body(...),
    new_content: str = Body(...)
):
    index = find_post_id_index(id)
    current_post = my_posts[index]

    current_post["id"] = id
    current_post["title"] = new_title
    current_post["content"] = new_content

    return f"title: {current_post['title']} content: {current_post['content']}"
