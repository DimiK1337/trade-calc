from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ANY SETTINGS CHANGED IN THE .env file need to be changed here
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./dev.db"

    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # comma-separated list
    CORS_ORIGINS: str = "http://localhost:3000"


settings = Settings()
