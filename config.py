from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    DEFAULT_POSITION_SIZE: float = 10000
    DEFAULT_LEVERAGE: float = 10
    DEFAULT_MIN_PNL: float = 1.0
    DEFAULT_CHECK_INTERVAL_SEC: int = 10

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
