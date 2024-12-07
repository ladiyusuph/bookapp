from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid
import logging
from src.config import Config


password_context = CryptContext(schemes=["bcrypt"])
TOKEN_EXPIRY = 3600.0

def generate_password_hash(password: str) -> str:
    pass_hash = password_context.hash(password)

    return pass_hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_token(user_data:dict, expiry:timedelta = None, refresh:bool=False):
    payload = {}
    
    payload["user"] = user_data
    expiry = expiry if expiry else timedelta(seconds=TOKEN_EXPIRY)
    payload["exp"] = datetime.now() + expiry
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    
    return token


def decode_token(token_str:str) -> dict:
    try:
        token = jwt.decode(
            jwt=token_str,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        
        return token
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
        