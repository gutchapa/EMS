
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas
from app.security_utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Body

auth_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register", response_model=schemas.UserOut)
def register(u: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == u.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    user = models.User(email=u.email, hashed_password=hash_password(u.password), role=u.role, full_name=u.full_name)
    db.add(user); db.commit(); db.refresh(user)
    return user

@auth_router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({ "sub": str(user.id), "role": user.role })
    return { "access_token": token, "token_type": "bearer" }
