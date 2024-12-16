from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.main import get_session
from src.auth.services import UserService
from .utils import decode_token
from .redis import jti_in_blacklist
from .models import User


user_service = UserService()
class AuthorizationCredential(HTTPBearer):
    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        
        if not self.validate_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Expired or Invalid Access token"
            )
            
        if await jti_in_blacklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"Error":"Token is Expired or Revoked",
                        "Resolution": "Please get a new token"}
            )
        self.verify_token_data(token_data)
            
        
        return token_data
    
    def validate_token(self, token_str:str) -> bool:
        
        decoded_token = decode_token(token_str)
        
        return True if decoded_token else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes !!")
    
class AcessTokenBearer(AuthorizationCredential):
    
    def verify_token_data(self, token_data):
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )
            
class RefreshTokenBearer(AuthorizationCredential):
    def verify_token_data(self, token_data):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )
            
            
async def get_current_user(
    token_details: dict = Depends(AcessTokenBearer()),
    session:AsyncSession = Depends(get_session)   
):
    user = await user_service.get_user_by_email(token_details['user']['email'], session)
    
    return user


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user:User = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to carry out this action"
        )