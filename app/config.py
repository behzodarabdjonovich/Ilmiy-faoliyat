from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-5.6-luna"
    database_url: str
    admin_ids: str = ""
    log_level: str = "INFO"
    max_input_length: int = 6000
    max_logo_size_mb: int = 5
    ai_request_timeout: int = 45
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def admins(self) -> set[int]:
        return {int(x.strip()) for x in self.admin_ids.split(",") if x.strip().isdigit()}

@lru_cache
def get_settings() -> Settings:
    return Settings()
