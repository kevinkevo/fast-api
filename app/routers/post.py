from .. import models,schemas,utils,auth2
from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from typing import Optional, List
from ..schemas import PostCreate, PostResponse,PostOut
from sqlalchemy.orm import Session
from ..database import engine,Base,get_db
from .. import models
from sqlalchemy import func

router = APIRouter(
    tags=["Posts"]
)

@router.get("/get", response_model= List[PostOut],)
def get_posts(db: Session = Depends (get_db),current_user:int = Depends(auth2.get_current_user),
              limit :int = 20, skip : int = 0, search : Optional[str]=""):#working with Object relational mapping (ORM)
    #cursor.execute(""" SELECT * FROM posts """)#the commented code is for working with regular sql
    #posts = cursor.fetchall()
    
    print(current_user)
    #posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                         models.Vote.post_id == models.Post.id, 
                         isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def create_post(post : PostCreate,db: Session = Depends (get_db),current_user:int = Depends(auth2.get_current_user)):#get_de function connects to the database
    #cursor.execute(""" INSERT INTO posts (title, content) VALUES(%s,%s) RETURNING * """,
                   #(post.title,post.content))
    #new_post = cursor.fetchone()
    #conn.commit()

    #return {"data": new_post }
   
    new_post = models.Post(owner_id= current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.get("/get/{id}",response_model=PostOut)
def get_post(id:int, db: Session = Depends (get_db),user_id:int = Depends(auth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    #post = cursor.fetchone()
    print(user_id)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                         models.Vote.post_id == models.Post.id, 
                         isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    return post



@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends (get_db),current_user:int = Depends(auth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authourized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}",response_model=PostResponse)
def update_post(id, response:Response, updated_post: PostCreate,db: Session = Depends (get_db),current_user:int = Depends(auth2.get_current_user)):#post:post_schema in regula sql
    #cursor.execute(""" UPDATE  posts SET title = %s, content = %s WHERE id = %s RETURNING *""",(post.title, post.content, str(id)))
    #updated_post =  cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"message": f"post with id:{id} does not exist"}
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authourized to perform requested action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return  post_query.first()