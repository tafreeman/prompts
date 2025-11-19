# Enterprise AI Prompt Library - Docker Deployment

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts

# Build and run
docker-compose -f deployment/docker/docker-compose.yml up -d

# Access the application
open http://localhost:5000
```

### Using Docker directly

```bash
# Build the image
docker build -f deployment/docker/Dockerfile -t prompt-library .

# Run the container
docker run -d -p 5000:5000 --name prompt-library prompt-library

# Access the application
open http://localhost:5000
```

## Deployment to Cloud Platforms

### AWS ECS (Elastic Container Service)

1. **Push image to ECR**:

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -f deployment/docker/Dockerfile -t prompt-library .
docker tag prompt-library:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest

# Push to ECR
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest
```

1. **Create ECS Task Definition** (see AWS section below)

### Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name prompt-library-rg --location eastus

# Create container registry
az acr create --resource-group prompt-library-rg --name promptlibraryacr --sku Basic

# Build and push to ACR
az acr build --registry promptlibraryacr --image prompt-library:latest -f deployment/docker/Dockerfile .

# Deploy to Container Instances
az container create \
  --resource-group prompt-library-rg \
  --name prompt-library \
  --image promptlibraryacr.azurecr.io/prompt-library:latest \
  --dns-name-label prompt-library-demo \
  --ports 5000
```

### Google Cloud Run

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/prompt-library -f deployment/docker/Dockerfile .

# Deploy to Cloud Run
gcloud run deploy prompt-library \
  --image gcr.io/YOUR_PROJECT_ID/prompt-library \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

## Environment Variables

Configure these in your deployment:

```bash
FLASK_ENV=production
FLASK_APP=app.py
DATABASE_PATH=/app/data/prompt_library.db
```

## Data Persistence

The database is stored in `/app/data/prompt_library.db`. Use volumes to persist data:

```bash
docker run -d \
  -p 5000:5000 \
  -v prompt_data:/app/data \
  --name prompt-library \
  prompt-library
```

## Scaling

### Docker Compose Scaling

```bash
docker-compose up -d --scale web=3
```

### Kubernetes Deployment

See `deployment/kubernetes/` for Kubernetes manifests.

## Health Checks

The container includes a health check endpoint at `/`:

```bash
curl http://localhost:5000/
```

## Logs

```bash
# View logs
docker logs prompt-library

# Follow logs
docker logs -f prompt-library
```

## Maintenance

### Backup Database

```bash
# Copy database from container
docker cp prompt-library:/app/data/prompt_library.db ./backup_$(date +%Y%m%d).db
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose -f deployment/docker/docker-compose.yml up -d --build
```

## Troubleshooting

### Container won't start

Check logs:

```bash
docker logs prompt-library
```

### Permission errors

Ensure volumes have correct permissions:

```bash
docker run -it --rm -v prompt_data:/data alpine chmod -R 777 /data
```

### Database initialization fails

Manually initialize:

```bash
docker exec -it prompt-library python load_prompts.py
```

## Security

1. **Use HTTPS**: Put behind reverse proxy (nginx, traefik)
2. **Environment variables**: Use secrets management
3. **Network**: Use Docker networks for isolation
4. **Updates**: Regularly rebuild images with latest dependencies

## Cost Optimization

### AWS (Approximate costs)

- **ECS Fargate**: ~$15-30/month (0.25 vCPU, 0.5GB RAM)
- **Lightsail Container**: $7/month (512MB RAM, 0.25 vCPU)

### Azure (Approximate costs)

- **Container Instances**: ~$10-20/month (0.5 vCPU, 1GB RAM)
- **App Service**: $13/month (Basic tier)

### Google Cloud (Approximate costs)

- **Cloud Run**: Pay per request, ~$5-15/month for low traffic

For minimal costs, use:

1. AWS Lightsail Container Service ($7/month)
2. Azure Container Instances with reserved pricing
3. Google Cloud Run (often within free tier for low traffic)
