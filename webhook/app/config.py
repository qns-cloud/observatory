"""
Configuration for the webhook service.
"""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the webhook service.
    """
    # Server settings
    host: str = "0.0.0.0"
    port: int = 9997
    debug: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Prometheus settings
    prometheus_url: str = os.environ.get("PROMETHEUS_URL", "http://prometheus:9090")
    
    # Alertmanager settings
    alertmanager_url: str = os.environ.get("ALERTMANAGER_URL", "http://alertmanager:9093")
    
    # External integration settings
    slack_webhook_url: str = os.environ.get("SLACK_WEBHOOK_URL", "")
    teams_webhook_url: str = os.environ.get("TEAMS_WEBHOOK_URL", "")
    pagerduty_routing_key: str = os.environ.get("PAGERDUTY_ROUTING_KEY", "")
    
    # Prefect settings
    prefect_api_url: str = os.environ.get("PREFECT_API_URL", "")
    prefect_api_key: str = os.environ.get("PREFECT_API_KEY", "")
    
    class Config:
        """
        Pydantic config.
        """
        env_file = ".env"


settings = Settings()