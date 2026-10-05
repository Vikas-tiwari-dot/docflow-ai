from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.core.security import decode_token

bearer=HTTPBearer(auto_error=False)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"success":False,"error":{"code":"UNAUTHORIZED","message":"Authentication required."}})
    payload=decode_token(credentials.credentials)
    if not payload or not payload.get("sub"): raise HTTPException(status_code=401, detail={"success":False,"error":{"code":"INVALID_TOKEN","message":"Invalid or expired token."}})
    user=db.get(User,int(payload["sub"]))
    if not user: raise HTTPException(status_code=401, detail={"success":False,"error":{"code":"USER_NOT_FOUND","message":"User no longer exists."}})
    return user
