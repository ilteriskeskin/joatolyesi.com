"""VAPID anahtar çifti üretir (bir kez çalıştırılır).

    python scripts/generate_vapid_keys.py

Çıktıyı .env'e VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY olarak yapıştır.
Public key, tarayıcının PushManager.subscribe() çağrısında applicationServerKey
olarak kullandığı ham (uncompressed point) base64url formatındadır.
"""

import base64

from cryptography.hazmat.primitives import serialization
from py_vapid import Vapid02


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def main() -> None:
    vapid = Vapid02()
    vapid.generate_keys()

    public_bytes = vapid.public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    private_value = vapid.private_key.private_numbers().private_value
    private_bytes = private_value.to_bytes(32, "big")

    print("VAPID_PUBLIC_KEY=" + _b64url(public_bytes))
    print("VAPID_PRIVATE_KEY=" + _b64url(private_bytes))


if __name__ == "__main__":
    main()
