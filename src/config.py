from pydantic_settings import BaseSettings, SettingsConfigDict
import os
env_file = os.path.join(os.path.dirname(__file__), ".env")

print(env_file)

class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    REDIS_HOST : str = "localhost"
    REDIS_PORT : int = 6379
    
    model_config = SettingsConfigDict(
        env_file =env_file,
        extra="ignore"
    )
    

Config = Settings()