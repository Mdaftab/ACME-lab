# Greet Microservice

A simple greeting service that remembers user names using Redis.

## Local Development

### Requirements
- Python 3.6+
- Redis server

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis server
redis-server

# Run the application
python greet/greet.py
```

The application will be available at http://localhost:8080

## API Endpoints

- `GET /` - Get a greeting message
- `POST /` - Update the greeting name (JSON payload: `{"name": "YourName"}`)
- `GET /health` - Health check endpoint

## Docker Build

Build the Docker image:

```bash
docker build -t greet:latest .
```

Run the Docker container locally (requires Redis):

```bash
# Start Redis first
docker run -d --name redis -p 6379:6379 redis:6.2-alpine

# Start the greet service
docker run -d --name greet -p 8080:8080 --link redis:redis greet:latest
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster
- kubectl configured to connect to your cluster
- Container registry access (e.g., ECR)

### Deployment Steps

1. Push the Docker image to your registry:

```bash
# Tag the image
docker tag greet:latest ${ECR_REPO}/greet:latest

# Push to registry
docker push ${ECR_REPO}/greet:latest
```

2. Update the ECR repository reference in the deployment YAML:

```bash
# Replace ${ECR_REPO} with your actual ECR repository URL
sed -i 's|${ECR_REPO}|123456789012.dkr.ecr.us-west-2.amazonaws.com|g' k8s/greet-deployment.yaml
```

3. Apply the Kubernetes manifests:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy Redis
kubectl apply -f k8s/redis.yaml

# Deploy Greet application
kubectl apply -f k8s/greet-deployment.yaml

# Create ingress
kubectl apply -f k8s/ingress.yaml
```

4. Verify the deployment:

```bash
kubectl get pods -n greet
kubectl get svc -n greet
kubectl get ingress -n greet
```

The application will be accessible at https://greeting-api.acme.co once DNS propagates and certificates are issued. 