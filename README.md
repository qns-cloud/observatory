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

3. Build and push the webhook image (required for Docker Swarm deployment):

```bash
# Build the webhook image
docker build -t observatory/webhook:latest -f webhook/webhook.Dockerfile webhook/

# If deploying to a Docker Swarm cluster with multiple nodes, push the image to a registry
# docker tag observatory/webhook:latest your-registry.com/observatory/webhook:latest
# docker push your-registry.com/observatory/webhook:latest
# Then update the WEBHOOK_IMAGE in .env to your-registry.com/observatory/webhook:latest
```

4. Start the services:

For Docker Compose:
```bash
docker-compose up -d
```

For Docker Swarm:
```bash
docker stack deploy -c docker-compose.yml observatory
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

### Service Dependencies and Startup Order

The services in Observatory have dependencies on each other, which affects the order in which they start:

1. **Core Services** (start first):
   - Prometheus (metrics collection and storage)
   - Node Exporter (host metrics)
   - cAdvisor (container metrics)
   - Nautobot databases (PostgreSQL and Redis)

2. **Secondary Services** (depend on core services):
   - Alertmanager (depends on Prometheus)
   - Loki (depends on Prometheus for metrics export)
   - Telegraf (depends on Prometheus for metrics export)
   - Nautobot (depends on PostgreSQL and Redis)

3. **Tertiary Services** (depend on secondary services):
   - Grafana (depends on Prometheus, Loki, and Alertmanager)
   - Logstash (depends on Loki)
   - Webhook (depends on Alertmanager)

These dependencies are defined in the docker-compose.yml file using the `depends_on` directive, which ensures that services start in the correct order.

### Docker Swarm Deployment Notes

When deploying to Docker Swarm, keep in mind the following:

1. All images must be available to all nodes in the Swarm. Either use images from public registries or push your custom images to a private registry accessible by all nodes.

2. The `build` directive is not supported in Docker Swarm mode. All services must use pre-built images.

3. Volumes are not automatically shared between nodes. For production deployments, consider using a shared storage solution or deploying stateful services with placement constraints.

4. Services with placement constraints (e.g., `node.role == manager`) will only run on manager nodes. Ensure you have enough manager nodes to handle these services.

5. The `depends_on` directive is respected in Docker Swarm, but it only affects the order in which services are created, not the order in which they become fully operational. For robust dependency handling, services should be designed to retry connections to their dependencies.

6. Health checks are important for ensuring services are fully operational. While Docker Swarm supports health checks, they don't affect service startup order in the same way as in Docker Compose. The services in Observatory are configured to be resilient to temporary unavailability of their dependencies, but you may need to adjust timeouts or implement additional retry logic for your specific environment.

7. To label a node for monitoring (required by some placement constraints):
   ```bash
   docker node update --label-add monitoring=true <node-id>
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.