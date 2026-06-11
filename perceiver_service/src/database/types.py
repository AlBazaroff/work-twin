import json
from typing import Any

from cryptography.fernet import Fernet
from sqlalchemy import Dialect, TypeDecorator, String

from config import get_settings

settings = get_settings()
SECRET = settings.secret_key
cipher = Fernet(SECRET)


class EncryptedString(TypeDecorator):
    """Encrypt string when recording, decrypt when extracting."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if value is not None:
            encrypted = cipher.encrypt(value.encode())
            return encrypted.decode()
        return value

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> Any | None:
        if value is not None:
            decrypted = cipher.decrypt(value)
            return decrypted.decode()
        return value


class EncryptedJSON(TypeDecorator):
    """Encrypt JSON when recording, decrypt when extracting."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if value is not None:
            json_data = json.dumps(value)
            encrypted = cipher.encrypt(json_data.encode())
            return encrypted.decode()
        return value

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> Any | None:
        if value is not None:
            decrypted = cipher.decrypt(value)
            result = json.loads(decrypted.decode())
            return result
        return value
