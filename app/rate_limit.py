from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

# Testte tüm istekler tek "IP" üzerinden aynı process'te aktığı için gerçek
# limitler saniyeler içinde aşılır; ENV=test iken kota devre dışı bırakılır.
limiter = Limiter(key_func=get_remote_address, enabled=settings.env != "test")
