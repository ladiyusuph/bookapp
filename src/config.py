from pydantic_settings import BaseSettings, SettingsConfigDict
import os
env_file = os.path.join(os.path.dirname(__file__), ".env")

print(env_file)

class Settings(BaseSettings):
    DATABASE_URL : str
    
    model_config = SettingsConfigDict(
        env_file =env_file,
        extra="ignore"
    )
    

Config = Settings()