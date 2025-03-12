# Network Observability Stack

This repository contains a **Docker Swarm-based observability stack** for **network monitoring, alerting, and automation**.

## 🚀 Components
- **Nautobot**: Stores network inventory data.
- **Alertmanager**: Sends alerts to external n8n.
- **Loki**: Stores and indexes network logs.
- **Logstash**: Collects syslogs and sends them to Loki.
- **Grafana**: Visualizes logs and network data.
- **Prometheus**: Collects metrics from Node Exporter.