"""Base settings for service."""

# LOGGING

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 32,
            "default_value": "-",
        },
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(correlation_id)s] [%(name)s] %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": ("correlation_id",),
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filters": ("correlation_id",),
            "filename": "perceiver.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "loggers": {
        "app": {
            "handlers": ("console", "file"),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ("console", "file"),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ("console", "file"),
            "level": "INFO",
            "propagate": False,
        },
    },
}
