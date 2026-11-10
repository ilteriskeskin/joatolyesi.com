"""Test ayarları. DB'li testler için Postgres gerekir:

    docker run -d --rm --name joryu-test-pg -e POSTGRES_PASSWORD=t \
      -e POSTGRES_USER=t -e POSTGRES_DB=t -p 127.0.0.1:55432:5432 postgres:16-alpine
    pytest

TEST_DATABASE_URL ile farklı bir DB gösterilebilir.
"""

import os
import subprocess
import sys

import pytest

os.environ.setdefault(
    "DATABASE_URL",
    os.environ.get("TEST_DATABASE_URL", "postgresql+asyncpg://t:t@127.0.0.1:55432/t"),
)
os.environ.setdefault("ADMIN_TOKEN", "test-admin-token")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENV", "test")
os.environ.setdefault("WAITLIST_ONLY", "false")
os.environ.setdefault("RESEND_API_KEY", "")  # mail gönderme, logla
# setdefault değil atama: env değişkeni .env'nin önüne geçer; sitemap/robots testleri
# yerel .env'ye ya da .env'nin yokluğuna bağlı olmadan kanonik alan adını görmeli
os.environ["BASE_URL"] = "https://joatolyesi.com"


@pytest.fixture(scope="session")
def migrated_db():
    """Şemayı alembic ile kurar; Postgres ayakta değilse DB testleri atlanır."""
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        env={**os.environ, "PYTHONPATH": "."},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"Test Postgres'i yok veya migration başarısız: {result.stderr[-300:]}")
    return True
