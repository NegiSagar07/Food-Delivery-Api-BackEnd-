from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Load all environmental veriable from the .env file

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()