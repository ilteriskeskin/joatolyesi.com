from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    # True iken sadece landing + waitlist açık; login/register ve app kapalı
    waitlist_only: bool = False
    database_url: str
    admin_token: str
    secret_key: str
    # Hata izleme — boşsa Sentry devre dışı
    sentry_dsn: str = ""
    # PWA push bildirimi (Web Push / VAPID) — boşsa push devre dışı, e-posta yeterli
    vapid_public_key: str = ""
    vapid_private_key: str = ""
    vapid_claims_email: str = "mailto:aliilteriskeskin@gmail.com"
    # E-posta (Resend) — boşsa mail gönderilmez, sadece loglanır (dev)
    resend_api_key: str = ""
    mail_from: str = "Joryu <noreply@joatolyesi.com>"
    base_url: str = "http://localhost:8000"
    ls_webhook_secret: str = ""
    ls_checkout_url_monthly: str = ""
    ls_checkout_url_yearly: str = ""


settings = Settings()
