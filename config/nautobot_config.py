import os
import sys

# Django settings
SECRET_KEY = os.environ.get("NAUTOBOT_SECRET_KEY", "observatory")
ALLOWED_HOSTS = ["*"]
DEBUG = os.environ.get("NAUTOBOT_DEBUG", "False").lower() == "true"

# Database
DATABASES = {
    "default": {
        "NAME": os.environ.get("NAUTOBOT_POSTGRES_DB", "nautobot"),
        "USER": os.environ.get("NAUTOBOT_POSTGRES_USER", "nautobot"),
        "PASSWORD": os.environ.get("NAUTOBOT_POSTGRES_PASSWORD", "nautobot"),
        "HOST": os.environ.get("NAUTOBOT_POSTGRES_HOST", "nautobot-postgres"),
        "PORT": os.environ.get("NAUTOBOT_POSTGRES_PORT", "5432"),
        "ENGINE": "django.db.backends.postgresql",
    }
}

# Redis
REDIS = {
    "tasks": {
        "HOST": os.environ.get("NAUTOBOT_REDIS_HOST", "nautobot-redis"),
        "PORT": int(os.environ.get("NAUTOBOT_REDIS_PORT", "6379")),
        "PASSWORD": os.environ.get("NAUTOBOT_REDIS_PASSWORD", "nautobot"),
        "DATABASE": int(os.environ.get("NAUTOBOT_REDIS_DATABASE", "0")),
        "SSL": os.environ.get("NAUTOBOT_REDIS_SSL", "False").lower() == "true",
    },
    "caching": {
        "HOST": os.environ.get("NAUTOBOT_REDIS_HOST", "nautobot-redis"),
        "PORT": int(os.environ.get("NAUTOBOT_REDIS_PORT", "6379")),
        "PASSWORD": os.environ.get("NAUTOBOT_REDIS_PASSWORD", "nautobot"),
        "DATABASE": int(os.environ.get("NAUTOBOT_REDIS_DATABASE", "1")),
        "SSL": os.environ.get("NAUTOBOT_REDIS_SSL", "False").lower() == "true",
    },
}

# Metrics
METRICS_ENABLED = True

# Plugins
PLUGINS = [
    "nautobot_plugin_prometheus_sd",
]

PLUGINS_CONFIG = {
    "nautobot_plugin_prometheus_sd": {
        "prometheus_url": "http://prometheus:9090",
    },
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)s: %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "normal",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "nautobot": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}