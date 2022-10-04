from typing import Optional
from pydantic import BaseSettings, PostgresDsn, validator
import configparser

class Config(BaseSettings):
    bot_token: str
    bot_fsm_storage: str
    postgres_dsn: PostgresDsn
    admin_id: int
    release_time: str
    full_link: str
    channels_file: str
    custom_bot_api: Optional[str]
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    webhook_domain: Optional[str]
    webhook_path: Optional[str]

    @validator("bot_fsm_storage")
    def validate_bot_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
        return v
    
    @validator("release_time")
    def validate_release_time(cls, v):
        if v not in ('random', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            raise ValueError("Incorrect 'release_time' value. Must be in range (0, 10) or 'random'")
        return v
    
    @validator("webhook_path")
    def validate_webhook_path(cls, v, values):
        if values["webhook_domain"] and not v:
            raise ValueError("Webhook path is missing!")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

config = Config()

channels = []
parser = configparser.ConfigParser()
parser.read(config.channels_file, encoding='utf-8')
for channel in parser.sections():
    channels.append(
        {
            'name' : parser[channel]['Name'],
            'chat_id' : int(parser[channel]['ChatId']),
            'join_link' : parser[channel]['JoinLink'],
        }
    )