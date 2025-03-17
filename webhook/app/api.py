"""
API endpoints for the webhook service.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from .config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


async def forward_to_slack(alert: Dict[str, Any]) -> None:
    """
    Forward an alert to Slack.
    """
    if not settings.slack_webhook_url:
        logger.warning("Slack webhook URL not configured, skipping")
        return

    try:
        message = {
            "text": f"*Alert: {alert.get('labels', {}).get('alertname', 'Unknown')}*",
            "attachments": [
                {
                    "color": "#ff0000" if alert.get("status") == "firing" else "#00ff00",
                    "fields": [
                        {
                            "title": "Status",
                            "value": alert.get("status", "Unknown"),
                            "short": True,
                        },
                        {
                            "title": "Severity",
                            "value": alert.get("labels", {}).get("severity", "Unknown"),
                            "short": True,
                        },
                        {
                            "title": "Summary",
                            "value": alert.get("annotations", {}).get("summary", "No summary"),
                            "short": False,
                        },
                        {
                            "title": "Description",
                            "value": alert.get("annotations", {}).get("description", "No description"),
                            "short": False,
                        },
                    ],
                }
            ],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.slack_webhook_url,
                json=message,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"Alert forwarded to Slack: {alert.get('labels', {}).get('alertname', 'Unknown')}")
    except Exception as e:
        logger.error(f"Failed to forward alert to Slack: {e}")


async def forward_to_teams(alert: Dict[str, Any]) -> None:
    """
    Forward an alert to Microsoft Teams.
    """
    if not settings.teams_webhook_url:
        logger.warning("Teams webhook URL not configured, skipping")
        return

    try:
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "ff0000" if alert.get("status") == "firing" else "00ff00",
            "summary": f"Alert: {alert.get('labels', {}).get('alertname', 'Unknown')}",
            "sections": [
                {
                    "activityTitle": f"Alert: {alert.get('labels', {}).get('alertname', 'Unknown')}",
                    "facts": [
                        {
                            "name": "Status",
                            "value": alert.get("status", "Unknown"),
                        },
                        {
                            "name": "Severity",
                            "value": alert.get("labels", {}).get("severity", "Unknown"),
                        },
                        {
                            "name": "Summary",
                            "value": alert.get("annotations", {}).get("summary", "No summary"),
                        },
                        {
                            "name": "Description",
                            "value": alert.get("annotations", {}).get("description", "No description"),
                        },
                    ],
                }
            ],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.teams_webhook_url,
                json=message,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"Alert forwarded to Teams: {alert.get('labels', {}).get('alertname', 'Unknown')}")
    except Exception as e:
        logger.error(f"Failed to forward alert to Teams: {e}")


async def forward_to_pagerduty(alert: Dict[str, Any]) -> None:
    """
    Forward an alert to PagerDuty.
    """
    if not settings.pagerduty_routing_key:
        logger.warning("PagerDuty routing key not configured, skipping")
        return

    try:
        event_action = "trigger" if alert.get("status") == "firing" else "resolve"
        severity = alert.get("labels", {}).get("severity", "warning")
        pd_severity = "critical" if severity == "critical" else "warning"

        message = {
            "routing_key": settings.pagerduty_routing_key,
            "event_action": event_action,
            "payload": {
                "summary": alert.get("annotations", {}).get("summary", "No summary"),
                "severity": pd_severity,
                "source": "Observatory",
                "component": alert.get("labels", {}).get("job", "Unknown"),
                "custom_details": {
                    "alertname": alert.get("labels", {}).get("alertname", "Unknown"),
                    "description": alert.get("annotations", {}).get("description", "No description"),
                    "instance": alert.get("labels", {}).get("instance", "Unknown"),
                },
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://events.pagerduty.com/v2/enqueue",
                json=message,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"Alert forwarded to PagerDuty: {alert.get('labels', {}).get('alertname', 'Unknown')}")
    except Exception as e:
        logger.error(f"Failed to forward alert to PagerDuty: {e}")


@router.post("/alert")
async def receive_alert(request: Request, background_tasks: BackgroundTasks) -> Dict[str, str]:
    """
    Receive an alert from Alertmanager and forward it to external systems.
    """
    try:
        payload = await request.json()
        logger.info(f"Received alert: {payload}")

        alerts = payload.get("alerts", [])
        for alert in alerts:
            background_tasks.add_task(forward_to_slack, alert)
            background_tasks.add_task(forward_to_teams, alert)
            background_tasks.add_task(forward_to_pagerduty, alert)

        return {"status": "success", "message": f"Processed {len(alerts)} alerts"}
    except Exception as e:
        logger.error(f"Failed to process alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}