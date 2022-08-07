from pydantic import BaseSettings, PostgresDsn, validator
import configparser

class Config(BaseSettings):
    bot_token: str
    bot_fsm_storage: str
    postgres_dsn: PostgresDsn
    admin_id: int
    channels_file: str

    @validator("bot_fsm_storage")
    def validate_bot_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
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
        [
            parser[channel]['Name'],
            int(parser[channel]['ChatId']),
            parser[channel]['JoinLink'],
        ]
    )