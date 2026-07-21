from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str

    HOST: str
    PORT: int

    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    SECRET_KEY: str

    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"


settings = Settings()