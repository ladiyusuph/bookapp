import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

token_blacklist = redis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)


async def add_jti_to_blacklist(token_jti:str):
    await token_blacklist.set(
        name=token_jti,
        value="",
        ex=JTI_EXPIRY
    )
    
    
async def jti_in_blacklist(token_jti:str) -> bool:
    jti = await token_blacklist.get(token_jti)
    
    return jti is not None