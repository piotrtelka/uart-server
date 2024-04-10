from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    device_port: str
    baud_rate: int
    pool_size: int = 4
