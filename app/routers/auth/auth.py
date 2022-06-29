from . import schemas
from ...database import database, models
from ...utils import password_functions, token_functions
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix='/auth', tags=["Authorization"])

@router.post('/login', response_model=schemas.Token)
def login(body: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if  user != None:
        matched: bool = password_functions.verify_password(body.password, user.password)
        if matched:
            access_token = token_functions.create_access_token(data={"id": user.userId})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Invalid credentials'
    )

@router.post('/register')
def register(body: schemas.Register, db: Session = Depends(database.get_db)):
    query = db.query(models.User).filter(models.User.email == body.email)
    if query.first() != None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User with email {body.email} already exists'
        )
    new_user = models.User(**body.dict())
    new_user.password = password_functions.hash_password(body.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = token_functions.create_access_token(data={"id": new_user.userId})
    return {"access_token": access_token, "token_type": "bearer"}
