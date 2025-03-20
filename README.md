# ACME DevOps Infrastructure and Implementation

This repository contains the DevOps infrastructure implementation for ACME Inc., including:

1. Infrastructure deployment plan and architecture
2. Containerized microservices
3. Kubernetes deployment manifests

## Repository Structure

- **Infrastructure Plan**: DevOps infrastructure and deployment strategy documentation
- **greet-service/**: Implementation of the 7th microservice - "Greet"
  - Containerized application
  - Kubernetes deployment manifests
  - CI/CD pipeline configuration

## Greet Microservice

The Greet service is a simple greeting API that remembers user names using Redis as a backend. 

### Key Features

- Containerized with Docker
- Configured for Kubernetes deployment
- Includes Redis dependency
- Accessible via HTTPS at greeting-api.acme.co
- Includes health checks and resource limits

See the [Greet Service README](greet-service/README.md) for detailed implementation and deployment instructions. - In-memory storage fallback for development without Redis
