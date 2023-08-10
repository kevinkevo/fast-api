from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from ..database import engine,Base,get_db
from sqlalchemy.orm import Session
from ..schemas import UserLogin
from . .import models,utils,auth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends (get_db)):
    user =db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail= f"invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    access_token = auth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type": "bearer"}
