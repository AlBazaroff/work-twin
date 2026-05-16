"""Shared pytest fixtures and test environment setup."""

import os

from cryptography.fernet import Fernet

# Settings and encrypted column types load at import time; set env first.
os.environ.setdefault("SECRET_KEY", Fernet.generate_key().decode())
os.environ.setdefault("RABBITMQ__USER", "guest")
os.environ.setdefault("RABBITMQ__PASSWORD", "guest")
os.environ.setdefault("RABBITMQ__HOSTNAME", "localhost")
os.environ.setdefault("RABBITMQ__PORT", "5672")
os.environ.setdefault("TELEGRAM__API_ID", "12345")
os.environ.setdefault("TELEGRAM__API_HASH", "test_api_hash")
os.environ.setdefault(
    "DATABASE__CONNECTION_URL", "sqlite+aiosqlite:///:memory:"
)
