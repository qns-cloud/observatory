import os

# More specific allowed hosts for security
ALLOWED_HOSTS = ["nautobot", "localhost", "127.0.0.1"]
DEBUG = False

# Enable metrics for Prometheus
METRICS_ENABLED = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAUTOBOT_DB_NAME", "nautobot"),
        "USER": os.getenv("NAUTOBOT_DB_USER", "nautobot"),
        "PASSWORD": os.getenv("NAUTOBOT_DB_PASSWORD", "nautobot"),
        "HOST": os.getenv("NAUTOBOT_DB_HOST", "nautobot-db"),
        "PORT": os.getenv("NAUTOBOT_DB_PORT", "5432"),
    }
}

PLUGINS = ["nautobot_loki"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}