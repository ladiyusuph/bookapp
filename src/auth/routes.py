from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.database.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
from .services import UserService
from .schema import CreateUser, UserResponse, UserLogin
from .utils import verify_password, create_token
from .dependencies import RefreshTokenBearer, AcessTokenBearer, get_current_user, RoleChecker
from .redis import add_jti_to_blacklist


auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY = 3
general = Depends(RoleChecker(["admin","user"]))
admin_only = Depends(RoleChecker(["admin","user"]))

@auth_router.post("/signup", response_model = UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUser, session:AsyncSession = Depends(get_session)):
    user_exists = await user_service.get_user_by_email(user_data.email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email exists !!")

    new_user = await user_service.create_user(user_data, session)
    
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_info:UserLogin, session:AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(user_info.email, session)
    if user:
        valid_passwrd = verify_password(user_info.password, user.password)
        
        if valid_passwrd:
            access_token = create_token(
                user_data = {
                    "email":user.email,
                    "uid":str(user.uid),
                    "role":user.role
                }
            )
            refresh_token = create_token(
                user_data = {
                    "email":user.email,
                    "uid":str(user.uid),
                    "role":user.role
                },
                refresh=True,
                expiry = timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            
            return JSONResponse(
                content = {
                    "message":":Login Successful",
                    "email": user.email,
                    "uid":str(user.uid),
                    "access_token":access_token,
                    "refresh_token":refresh_token
                },
                status_code=status.HTTP_200_OK
            )
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password !!")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not exist, Register new user")
    
    
@auth_router.get("/refresh_token")
async def refresh_auth_token(token_data: dict = Depends(RefreshTokenBearer())):
    token_timestamp = token_data["exp"]
    
    if datetime.fromtimestamp(token_timestamp) > datetime.now():
        access_token = create_token(
            user_data=token_data["user"]
        )
        
        return JSONResponse(
            content={"access_token":access_token},
            status_code=status.HTTP_201_CREATED
        )
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired token")
    
@auth_router.post("/logout")
async def user_logout(token_details: dict = Depends(AcessTokenBearer())):
    jti = token_details["jti"]
    
    await add_jti_to_blacklist(jti)
    
    return JSONResponse(
        content={"message":"Logout Successfull"},
        status_code=status.HTTP_200_OK
    )
    
@auth_router.post('/me', dependencies=[general])
async def get_user(user = Depends(get_current_user)):
    return user