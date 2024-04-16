from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, RedisDsn


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    bot_token: SecretStr
    teacher_telegram_id: int
    verbs_quantity_per_message: int
    verbs_challenge_hour: int
    verbs_challenge_minute: int
    verbs_challenge_days: str
    redemption_verbs_challenge_day: str
    redis_url: RedisDsn
    irregular_verbs_file_path: Path = BASE_DIR.parent / 'list_of_irregular_verbs.txt'
    verb_challenge_users_file: Path = BASE_DIR.parent / 'users_verb_challenge.json'
    

    model_config = SettingsConfigDict(env_file=BASE_DIR.parent/ '.env', env_file_encoding='utf-8')


config = Settings() # type: ignore
