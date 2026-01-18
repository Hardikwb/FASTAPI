import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Union

from fastapi import FastAPI, HTTPException,responses,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import models
from database import get_db,engine
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password='12345',cursor_factory=RealDictCursor)
        # realDict give column name and value
        cursor = conn.cursor()
        # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
        # cur.execute("SELECT * FROM test;")
        # cur.fetchone()
        print("Connected to DataBase successfully ! ")
        break
    except Exception as error:
        print("Connection to DataBase failed with error ",error)

class POST(BaseModel):
    title:str
    content:str
    published:bool=True


@app.get("/")
def read_root():
    return {"message": "Welcome to my world"}

# TODO TO research

# get_Db is there in database.py
@app.get('/sqlalchemy')
def test_post(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    print(type(posts))
    # print((posts))
    return posts


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return posts

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_posts(post: POST):
    try:
        cursor.execute(
            """
            INSERT INTO posts (title, content, published)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (post.title, post.content, post.published)
        )
        new_post = cursor.fetchone()
        conn.commit()
        return {"data": new_post}

    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
    
    
@app.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    try:
        cursor.execute(
            "SELECT * FROM posts WHERE id = %s returning *",
            (str(id),)
        )
        post = cursor.fetchone()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        return {"data": post}

    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
    

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        cursor.execute(
            "DELETE FROM posts WHERE id = %s returning *",
            ((id),)
        )
        post = cursor.fetchone()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        conn.commit()
        return

    except HTTPException:
        raise 
    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )

@app.put("/post/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,post:POST):
    try:
        cursor.execute(
            """UPDATE posts   SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published,id)
        )
        updated_post = cursor.fetchone()

        if updated_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        conn.commit()
        return {"data": updated_post}

    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )