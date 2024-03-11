from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    mysql_url: str
    mongo_url: str
    redis_url: str


class JWT(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiry_time: int


settings = Setting()

jwt_settings = JWT()
