# Enterprise AI Prompt Library - Azure Deployment Guide

## Deployment Options

### Option 1: Azure Container Instances (Easiest, ~$10-20/month)

Perfect for getting started quickly with minimal configuration.

```bash
# Login to Azure
az login

# Create resource group
az group create --name prompt-library-rg --location eastus

# Create container registry
az acr create \
  --resource-group prompt-library-rg \
  --name promptlibraryacr \
  --sku Basic

# Build and push image to ACR
az acr build \
  --registry promptlibraryacr \
  --image prompt-library:latest \
  --file deployment/docker/Dockerfile \
  .

# Enable admin access to ACR (for ACI)
az acr update --name promptlibraryacr --admin-enabled true

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name promptlibraryacr --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name promptlibraryacr --query passwords[0].value -o tsv)

# Deploy to Azure Container Instances
az container create \
  --resource-group prompt-library-rg \
  --name prompt-library \
  --image promptlibraryacr.azurecr.io/prompt-library:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server promptlibraryacr.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label prompt-library-demo \
  --ports 5000 \
  --environment-variables FLASK_ENV=production

# Get the FQDN
az container show \
  --resource-group prompt-library-rg \
  --name prompt-library \
  --query ipAddress.fqdn \
  --output tsv
```

**Cost**: ~$10-20/month (1 vCPU, 1GB RAM)

### Option 2: Azure App Service (Recommended, ~$13-55/month)

Better for production with built-in features like SSL, auto-scaling, and deployment slots.

#### Using Web App for Containers

```bash
# Create App Service plan
az appservice plan create \
  --name prompt-library-plan \
  --resource-group prompt-library-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group prompt-library-rg \
  --plan prompt-library-plan \
  --name prompt-library-app \
  --deployment-container-image-name promptlibraryacr.azurecr.io/prompt-library:latest

# Configure ACR credentials
az webapp config container set \
  --name prompt-library-app \
  --resource-group prompt-library-rg \
  --docker-custom-image-name promptlibraryacr.azurecr.io/prompt-library:latest \
  --docker-registry-server-url https://promptlibraryacr.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Configure environment variables
az webapp config appsettings set \
  --resource-group prompt-library-rg \
  --name prompt-library-app \
  --settings FLASK_ENV=production WEBSITES_PORT=5000

# Enable CI/CD from ACR
az webapp deployment container config \
  --enable-cd true \
  --name prompt-library-app \
  --resource-group prompt-library-rg

# Get URL
echo "App URL: https://prompt-library-app.azurewebsites.net"
```

**Cost**:

- Basic (B1): $13/month (1 core, 1.75GB RAM)
- Standard (S1): $55/month (1 core, 1.75GB RAM, auto-scale, deployment slots)

#### Using Python App Service (Alternative)

```bash
# Create App Service plan
az appservice plan create \
  --name prompt-library-plan \
  --resource-group prompt-library-rg \
  --sku B1 \
  --is-linux

# Create web app with Python runtime
az webapp create \
  --resource-group prompt-library-rg \
  --plan prompt-library-plan \
  --name prompt-library-app \
  --runtime "PYTHON:3.11"

# Deploy from local Git
az webapp deployment source config-local-git \
  --name prompt-library-app \
  --resource-group prompt-library-rg

# Configure startup command
az webapp config set \
  --resource-group prompt-library-rg \
  --name prompt-library-app \
  --startup-file "cd src && gunicorn --bind 0.0.0.0:8000 --workers 4 app:app"

# Add remote and push
git remote add azure <GIT_URL_FROM_PREVIOUS_COMMAND>
git push azure main
```

### Option 3: Azure Kubernetes Service (AKS, ~$70+/month)

For enterprise-grade deployments with high availability.

```bash
# Create AKS cluster
az aks create \
  --resource-group prompt-library-rg \
  --name prompt-library-aks \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-managed-identity \
  --attach-acr promptlibraryacr

# Get credentials
az aks get-credentials \
  --resource-group prompt-library-rg \
  --name prompt-library-aks

# Deploy application (using kubectl)
kubectl apply -f deployment/kubernetes/
```

**Cost**: ~$70+/month (2 x Standard_B2s nodes)

## Database Persistence

### Using Azure Files (Recommended for ACI)

```bash
# Create storage account
az storage account create \
  --resource-group prompt-library-rg \
  --name promptlibrarystorage \
  --sku Standard_LRS

# Create file share
az storage share create \
  --name promptdata \
  --account-name promptlibrarystorage

# Get storage key
STORAGE_KEY=$(az storage account keys list \
  --resource-group prompt-library-rg \
  --account-name promptlibrarystorage \
  --query "[0].value" -o tsv)

# Deploy ACI with mounted volume
az container create \
  --resource-group prompt-library-rg \
  --name prompt-library \
  --image promptlibraryacr.azurecr.io/prompt-library:latest \
  --azure-file-volume-account-name promptlibrarystorage \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name promptdata \
  --azure-file-volume-mount-path /app/data
```

### Using Azure Blob Storage for Backups

```bash
# Create container in storage account
az storage container create \
  --name backups \
  --account-name promptlibrarystorage

# Install Azure Storage SDK in application
pip install azure-storage-blob

# Add backup script to application
# See deployment/azure/backup_script.py
```

## Custom Domain and SSL

### Add Custom Domain

```bash
# Add custom domain to App Service
az webapp config hostname add \
  --webapp-name prompt-library-app \
  --resource-group prompt-library-rg \
  --hostname prompts.yourcompany.com

# Bind SSL certificate
az webapp config ssl upload \
  --certificate-file path/to/cert.pfx \
  --certificate-password PASSWORD \
  --name prompt-library-app \
  --resource-group prompt-library-rg

az webapp config ssl bind \
  --certificate-thumbprint THUMBPRINT \
  --ssl-type SNI \
  --name prompt-library-app \
  --resource-group prompt-library-rg
```

### Use Azure Managed SSL (Free)

```bash
# Create managed certificate (requires custom domain)
az webapp config ssl create \
  --resource-group prompt-library-rg \
  --name prompt-library-app \
  --hostname prompts.yourcompany.com

az webapp config ssl bind \
  --certificate-thumbprint THUMBPRINT \
  --ssl-type SNI \
  --name prompt-library-app \
  --resource-group prompt-library-rg
```

## Monitoring and Logging

### Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app prompt-library-insights \
  --location eastus \
  --resource-group prompt-library-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app prompt-library-insights \
  --resource-group prompt-library-rg \
  --query instrumentationKey -o tsv)

# Add to app settings
az webapp config appsettings set \
  --resource-group prompt-library-rg \
  --name prompt-library-app \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### View Logs

```bash
# Enable application logging
az webapp log config \
  --name prompt-library-app \
  --resource-group prompt-library-rg \
  --application-logging filesystem

# Stream logs
az webapp log tail \
  --name prompt-library-app \
  --resource-group prompt-library-rg
```

## Auto-Scaling

### App Service Auto-Scale

```bash
# Create autoscale setting
az monitor autoscale create \
  --resource-group prompt-library-rg \
  --resource prompt-library-app \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-setting \
  --min-count 1 \
  --max-count 4 \
  --count 1

# Create scale-out rule
az monitor autoscale rule create \
  --resource-group prompt-library-rg \
  --autoscale-name autoscale-setting \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1

# Create scale-in rule
az monitor autoscale rule create \
  --resource-group prompt-library-rg \
  --autoscale-name autoscale-setting \
  --condition "Percentage CPU < 30 avg 5m" \
  --scale in 1
```

## Deployment Slots (App Service only)

```bash
# Create staging slot
az webapp deployment slot create \
  --name prompt-library-app \
  --resource-group prompt-library-rg \
  --slot staging

# Deploy to staging
az webapp deployment source config \
  --name prompt-library-app \
  --resource-group prompt-library-rg \
  --slot staging \
  --repo-url https://github.com/tafreeman/prompts \
  --branch main

# Swap staging to production
az webapp deployment slot swap \
  --name prompt-library-app \
  --resource-group prompt-library-rg \
  --slot staging \
  --target-slot production
```

## Continuous Deployment

### Using Azure DevOps

Create `azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Docker@2
  inputs:
    containerRegistry: 'promptlibraryacr'
    repository: 'prompt-library'
    command: 'buildAndPush'
    Dockerfile: '**/deployment/docker/Dockerfile'

- task: AzureWebAppContainer@1
  inputs:
    azureSubscription: 'Azure-Connection'
    appName: 'prompt-library-app'
    containers: 'promptlibraryacr.azurecr.io/prompt-library:$(Build.BuildId)'
```

### Using GitHub Actions

See `.github/workflows/deploy.yml` (already created)

To set up secrets:

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "prompt-library-github" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/prompt-library-rg \
  --sdk-auth

# Add output JSON to GitHub Secrets as AZURE_CREDENTIALS
```

## Cost Optimization Tips

1. **Start with Container Instances** ($10-20/month)
2. **Use App Service Basic tier** ($13/month) for production
3. **Enable auto-shutdown** for development environments
4. **Use Azure Hybrid Benefit** if you have Windows Server licenses
5. **Reserve instances** for 30-40% savings on long-term deployments
6. **Use consumption-based services** like Azure Functions for low-traffic apps

## Backup and Disaster Recovery

```bash
# Enable automated backups (App Service Standard/Premium only)
az webapp config backup create \
  --resource-group prompt-library-rg \
  --webapp-name prompt-library-app \
  --storage-account-url "https://promptlibrarystorage.blob.core.windows.net/backups?{SAS_TOKEN}" \
  --frequency 1d \
  --retain-one true \
  --retention 30

# Manual backup
az webapp config backup create \
  --resource-group prompt-library-rg \
  --webapp-name prompt-library-app \
  --backup-name manual-backup-$(date +%Y%m%d) \
  --storage-account-url "https://promptlibrarystorage.blob.core.windows.net/backups?{SAS_TOKEN}"
```

## Cleanup

```bash
# Delete everything
az group delete --name prompt-library-rg --yes --no-wait
```

## Support

- Azure Documentation: <https://docs.microsoft.com/azure/>
- App Service: <https://docs.microsoft.com/azure/app-service/>
- Container Instances: <https://docs.microsoft.com/azure/container-instances/>
