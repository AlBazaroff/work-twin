"""Base settings for service."""

# LOGGING

LOGGING_FILE_DEFAULT_SIZE = 10485760
LOGGING_FILE_DEFAULT_BACKUP_COUNT = 5

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
        "uv_access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s"
        },
        "uv_error": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s"
        }
    },
    "handlers": {
        "app_console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ("correlation_id",),
            "level": "DEBUG",
        },
        "app_file": {
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filters": ("correlation_id",),
            "filename": "/logs/perceiver.log",
            "maxBytes": LOGGING_FILE_DEFAULT_SIZE,
            "backupCount": LOGGING_FILE_DEFAULT_BACKUP_COUNT,
        },
        "uvicorn_console": {
            "formatter": "uv_access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "uvicorn_file": {
            "formatter": "uv_access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/logs/uvicorn.log",
            "maxBytes": LOGGING_FILE_DEFAULT_SIZE,
            "backupCount": LOGGING_FILE_DEFAULT_BACKUP_COUNT,
        },
        "uvicorn_error_console": {
            "formatter": "uv_error",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "uvicorn_error_file": {
            "formatter": "uv_error",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/logs/uvicorn-error.log",
            "maxBytes": LOGGING_FILE_DEFAULT_SIZE,
            "backupCount": LOGGING_FILE_DEFAULT_BACKUP_COUNT,
        },
    },
    "loggers": {
        "app": {
            "handlers": ("app_console", "app_file"),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ("uvicorn_console", "uvicorn_file"),
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ("uvicorn_error_console", "uvicorn_error_file"),
            "level": "INFO",
            "propagate": False,
        },
    },
}
