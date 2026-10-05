from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register",response_model=TokenResponse,status_code=201)
def register(payload:RegisterRequest,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==payload.email.lower()).first(): raise HTTPException(409,{"success":False,"error":{"code":"EMAIL_EXISTS","message":"An account with this email already exists."}})
    user=User(name=payload.name.strip(),email=payload.email.lower(),password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(user.id),"token_type":"bearer"}
@router.post("/login",response_model=TokenResponse)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email.lower()).first()
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(401,{"success":False,"error":{"code":"INVALID_CREDENTIALS","message":"Email or password is incorrect."}})
    return {"access_token":create_access_token(user.id),"token_type":"bearer"}
@router.post("/logout")
def logout(): return {"success":True,"message":"Logged out. Remove the client token."}
