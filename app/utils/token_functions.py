from ..config import settings
from ..database import database, models
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get("id")
        if userId != None:
            return userId
    except JWTError:
        pass
    raise credential_exception

def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
    db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    userId = verify_access_token(token, credential_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.userId == userId).first()
    return user
