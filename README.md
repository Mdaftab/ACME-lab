# Greet Microservice

A simple greeting service that remembers user names using Redis or in-memory storage. Part of the ACME Inc. microservices architecture.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Local Development](#local-development)
- [Docker Development](#docker-development)
- [API Reference](#api-reference)
- [Deployment Guide](#deployment-guide)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

## Overview

The Greet microservice provides a simple greeting API that can remember user names. It's designed to be:
- Highly available
- Horizontally scalable
- Cloud-native
- Development friendly

## Features

- 🚀 Simple REST API for greetings
- 💾 Redis-backed persistence with in-memory fallback
- 🐳 Docker containerization
- ☸️ Kubernetes deployment ready
- 🔄 GitHub Actions CI/CD pipeline
- 🔒 HTTPS support via ingress
- 🏗️ Dev-friendly local setup

## Architecture

### Components
- **API Server**: Flask-based REST API
- **Storage**: Redis (primary) with in-memory fallback
- **Container**: Docker with multi-stage builds
- **Orchestration**: Kubernetes deployment
- **Ingress**: NGINX Ingress Controller
- **CI/CD**: GitHub Actions pipeline

### Dependencies
- Python 3.6+
- Redis 6.2+
- Flask 2.0.1
- Werkzeug 2.0.1
- Gunicorn 20.1.0

## Local Development

### Prerequisites
- Python 3.6+
- Redis server (optional)
- pip or poetry

### Setup Without Docker

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Optional: Start Redis server:
```bash
redis-server
```

4. Run the application:
```bash
python -m greet.greet
```

The application will be available at http://localhost:8080

### Development Mode Features
- Automatic Redis detection
- In-memory fallback storage
- Debug mode enabled
- Hot reload support

## Docker Development

### Prerequisites
- Docker 20.10+
- Docker Compose v2+ (recommended)

### Using Docker Compose (Recommended)

1. Start the application stack:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the stack:
```bash
docker-compose down
```

### Manual Docker Setup

```bash
# Build image
docker build -t greet:latest .

# Start Redis
docker run -d --name redis -p 6379:6379 redis:6.2-alpine

# Start Greet service
docker run -d --name greet -p 8080:8080 --link redis:redis greet:latest
```

## API Reference

### Endpoints

#### GET /health
Health check endpoint
```bash
curl http://localhost:8080/health
```
Response:
```json
{
  "status": "healthy",
  "storage": "redis",
  "version": "1.0.0"
}
```

#### GET /
Get greeting message
```bash
curl http://localhost:8080/
```
Response:
```json
{
  "message": "Hello, {name}!"
}
```

#### POST /
Set user name
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"ACME DevOps"}' \
     http://localhost:8080/
```
Response:
```json
{
  "message": "I will remember your name, ACME DevOps!"
}
```

## Deployment Guide

### Prerequisites
- Kubernetes 1.20+
- kubectl configured
- Container registry access
- SSL certificate issuer (cert-manager)

### Environment Setup

1. Configure container registry:
```bash
# For AWS ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${ECR_REPO}
```

2. Build and push image:
```bash
# Build with version tag
docker build -t ${ECR_REPO}/greet:${VERSION} .

# Push to registry
docker push ${ECR_REPO}/greet:${VERSION}
```

### Kubernetes Deployment

1. Update deployment configuration:
```bash
# Set image version
sed -i "s|image:.*|image: ${ECR_REPO}/greet:${VERSION}|g" k8s/greet-deployment.yaml
```

2. Apply manifests:
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy Redis
kubectl apply -f k8s/redis.yaml

# Deploy application
kubectl apply -f k8s/greet-deployment.yaml

# Configure ingress
kubectl apply -f k8s/ingress.yaml
```

3. Verify deployment:
```bash
# Check pods
kubectl get pods -n greet

# Check services
kubectl get svc -n greet

# Check ingress
kubectl get ingress -n greet
```

### Post-Deployment Verification

1. Wait for DNS propagation
2. Verify HTTPS certificate
3. Test endpoints:
```bash
curl https://greeting-api.acme.co/health
```

## Monitoring & Logging

### Kubernetes Logs
```bash
# Get application logs
kubectl logs -n greet -l app=greet

# Get Redis logs
kubectl logs -n greet -l app=redis
```

### Metrics
- Application exposes Prometheus metrics at `/metrics`
- Redis metrics available through Redis exporter
- Kubernetes metrics via metrics-server

### Alerts
- Pod health checks
- Redis connection status
- Response time thresholds
- Error rate monitoring

## Troubleshooting

### Common Issues

1. Redis Connection Failures
   - Verify Redis pod status
   - Check network policies
   - Validate Redis service DNS
   - Application will fallback to in-memory storage

2. Pod Startup Issues
   - Check pod events: `kubectl describe pod -n greet <pod-name>`
   - Verify resource limits
   - Check image pull status

3. Ingress Issues
   - Verify ingress controller status
   - Check SSL certificate status
   - Validate DNS records

### Debug Commands

```bash
# Check pod status
kubectl get pods -n greet

# View pod logs
kubectl logs -n greet <pod-name>

# Check ingress status
kubectl describe ingress -n greet

# Port forward for local testing
kubectl port-forward -n greet svc/greet 8080:80
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For more details, see [CONTRIBUTING.md](../CONTRIBUTING.md) 