from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import get_settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALG = "HS256"
def hash_password(value): return pwd.hash(value)
def verify_password(plain, hashed): return pwd.verify(plain, hashed)
def create_access_token(user_id: int):
    s=get_settings(); exp=datetime.now(timezone.utc)+timedelta(minutes=s.jwt_expire_minutes)
    return jwt.encode({"sub":str(user_id),"exp":exp}, s.jwt_secret, algorithm=ALG)
def decode_token(token):
    s=get_settings()
    try: return jwt.decode(token, s.jwt_secret, algorithms=[ALG])
    except JWTError: return None
