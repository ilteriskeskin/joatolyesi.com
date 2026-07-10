from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    # True iken sadece landing + waitlist açık; login/register ve app kapalı
    waitlist_only: bool = False
    database_url: str
    admin_token: str
    secret_key: str
    ls_webhook_secret: str = ""
    ls_checkout_url_monthly: str = ""
    ls_checkout_url_yearly: str = ""


settings = Settings()
