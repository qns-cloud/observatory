# Observatory

Observatory is a comprehensive monitoring solution that combines the best features of various monitoring tools into a single, integrated stack.

## Components

### Core Monitoring

- **Prometheus**: Time series database for metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **Alertmanager**: Alert routing and notification
- **Node Exporter**: Host metrics collection
- **cAdvisor**: Container metrics collection

### Network Monitoring

- **Telegraf**: Network device metrics collection
- **Nautobot**: Network automation and source of truth

### Log Aggregation

- **Loki**: Log storage and querying
- **Logstash**: Log processing and forwarding

### Custom Components

- **Webhook Service**: Custom service for integrating with external systems

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Docker Swarm (optional, for production deployments)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/observatory.git
cd observatory
```

2. Create a `.env` file with the required environment variables:

```bash
# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# Nautobot
NAUTOBOT_POSTGRES_USER=nautobot
NAUTOBOT_POSTGRES_PASSWORD=nautobot
NAUTOBOT_POSTGRES_DB=nautobot
NAUTOBOT_REDIS_PASSWORD=nautobot

# Webhook Service
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/slack/webhook
TEAMS_WEBHOOK_URL=https://your-tenant.webhook.office.com/webhookb2/your/teams/webhook
PAGERDUTY_ROUTING_KEY=your-pagerduty-routing-key
```

3. Start the services:

```bash
docker-compose up -d
```

4. Access the services:

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Nautobot: http://localhost:8080

## Configuration

### Adding Dashboards

Place your dashboard JSON files in the `dashboards` directory:

- `dashboards/network/`: Network-related dashboards
- `dashboards/system/`: System-related dashboards
- `dashboards/logs/`: Log-related dashboards

### Customizing Alerts

Edit the `config/prometheus-alerts.yml` file to customize alerting rules.

### Configuring External Integrations

Edit the `.env` file to configure external integrations like Slack, Microsoft Teams, and PagerDuty.

## Architecture

Observatory is designed as a modular, containerized monitoring stack that can be deployed on a single host or across a Docker Swarm cluster.

The core components (Prometheus, Grafana, Alertmanager) provide the foundation for metrics collection, visualization, and alerting. Additional components extend the functionality to include network monitoring, log aggregation, and integration with external systems.

## License

This project is licensed under the MIT License - see the LICENSE file for details.