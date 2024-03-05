from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Setting(BaseSettings):
    mysql_url: str


settings = Setting()

