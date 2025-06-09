from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
import models
from database import engine,get_db  # Import Base and get_db
import schemas
from sqlalchemy.orm import Session
import auth,oauth2

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Get all posts
@app.get("/users", response_model=List[schemas.UserShow])
def get_user(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result


# Get an employee by ID
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@app.post("/users")
def add_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)):

    hashed_pass = auth.hash(user.password)
    user.password = hashed_pass
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

    return {"message": "Post added successfully"}



# Delete an employee by ID
@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"message": "Employee deleted successfully"}




#get all posts
# Get all posts
@app.get("/posts", response_model=List[schemas.PostShow])
def get_posts(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    result = db.query(models.Post).all()
    return result

# create a post
@app.post("/posts")
def add_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    print(current_user.id)

    db_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(db_post)
    db.commit()

    return {"message": "posts added successfully"}

@app.post("/login")
def user_login(usercred :OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == usercred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not auth.verify(usercred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = oauth2.create_access_token(data={"user_id" : user.id})
    return{"token": access_token,"token_type":"bearer"}