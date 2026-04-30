import json
from typing import Any

from cryptography.fernet import Fernet
from sqlalchemy import Dialect, TypeDecorator, String

import config

SECRET = config.CRYPTO_SECRET_KEY
cipher = Fernet(SECRET)


class EncryptedString(TypeDecorator):
    """Encrypt string column, decrypt when extracting."""

    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if value is not None:
            encrypted = cipher.encrypt(value)
            return encrypted
        return value

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> Any | None:
        if value is not None:
            decrypted = cipher.decrypt(value)
            return decrypted
        return value


class EncryptedJSON(TypeDecorator):
    """Encrypt JSON when recording, decrypted when extracting."""

    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if value is not None:
            json_str = json.dumps(value)
            encrypted = cipher.encrypt(json_str.encode())
            return encrypted
        return value

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> Any | None:
        if value is not None:
            decrypted = cipher.decrypt(value)
            result = json.loads(decrypted.decode())
            return result
        return value
