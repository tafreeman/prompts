# Enterprise AI Prompt Library - AWS Deployment Guide

## Deployment Options

### Option 1: AWS Lightsail (Easiest, ~$7/month)

Perfect for small teams and getting started quickly.

```bash
# 1. Create Lightsail container service
aws lightsail create-container-service \
  --service-name prompt-library \
  --power small \
  --scale 1

# 2. Push Docker image
aws lightsail push-container-image \
  --service-name prompt-library \
  --label prompt-library \
  --image prompt-library:latest

# 3. Deploy
aws lightsail create-container-service-deployment \
  --service-name prompt-library \
  --containers '{
    "prompt-app": {
      "image": ":prompt-library.latest",
      "ports": {
        "5000": "HTTP"
      }
    }
  }' \
  --public-endpoint '{
    "containerName": "prompt-app",
    "containerPort": 5000,
    "healthCheck": {
      "path": "/"
    }
  }'
```

**Cost**: $7/month (512MB RAM, 0.25 vCPU)

### Option 2: AWS ECS with Fargate (~$15-30/month)

Better for production environments with auto-scaling needs.

#### Step 1: Create ECR Repository

```bash
# Create repository
aws ecr create-repository --repository-name prompt-library --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -f deployment/docker/Dockerfile -t prompt-library .
docker tag prompt-library:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest
```

#### Step 2: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name prompt-library-cluster

# Create task execution role (if not exists)
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://deployment/aws/task-execution-role.json
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

#### Step 3: Create Task Definition

Save as `task-definition.json`:

```json
{
  "family": "prompt-library",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "prompt-library",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/prompt-library",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register the task:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Step 4: Create Service with Load Balancer

```bash
# Create security group
aws ec2 create-security-group \
  --group-name prompt-library-sg \
  --description "Security group for Prompt Library" \
  --vpc-id YOUR_VPC_ID

# Allow inbound HTTP
aws ec2 authorize-security-group-ingress \
  --group-id YOUR_SG_ID \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Create Application Load Balancer (optional but recommended)
aws elbv2 create-load-balancer \
  --name prompt-library-alb \
  --subnets YOUR_SUBNET_1 YOUR_SUBNET_2 \
  --security-groups YOUR_SG_ID

# Create target group
aws elbv2 create-target-group \
  --name prompt-library-tg \
  --protocol HTTP \
  --port 5000 \
  --vpc-id YOUR_VPC_ID \
  --target-type ip \
  --health-check-path /

# Create ECS service
aws ecs create-service \
  --cluster prompt-library-cluster \
  --service-name prompt-library-service \
  --task-definition prompt-library \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[YOUR_SUBNET_1,YOUR_SUBNET_2],securityGroups=[YOUR_SG_ID],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=YOUR_TG_ARN,containerName=prompt-library,containerPort=5000"
```

**Cost**: ~$15-30/month (0.25 vCPU, 0.5GB RAM)

### Option 3: AWS Elastic Beanstalk (~$20-40/month)

Simplest for teams familiar with Beanstalk.

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize Application

```bash
cd src
eb init -p docker prompt-library --region us-east-1
```

#### Step 3: Create Dockerrun.aws.json

```json
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/prompt-library:latest",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": 5000,
      "HostPort": 80
    }
  ]
}
```

#### Step 4: Deploy

```bash
eb create prompt-library-env
eb deploy
```

**Cost**: ~$20-40/month (t3.micro instance)

## Database Persistence

For production, use Amazon RDS or S3 for database:

### Using S3 for Database Backup

```bash
# Install AWS CLI in Dockerfile
RUN apt-get install -y awscli

# Add backup script
aws s3 cp /app/data/prompt_library.db s3://your-bucket/backups/prompt_library_$(date +%Y%m%d).db
```

### Using EFS for Persistent Storage

```bash
# Create EFS file system
aws efs create-file-system --creation-token prompt-library-db

# Mount in ECS task definition
{
  "volumes": [
    {
      "name": "database",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-xxxxx",
        "rootDirectory": "/"
      }
    }
  ],
  "mountPoints": [
    {
      "sourceVolume": "database",
      "containerPath": "/app/data"
    }
  ]
}
```

## Custom Domain Setup

### Using Route 53

```bash
# Create hosted zone
aws route53 create-hosted-zone --name prompts.yourcompany.com --caller-reference $(date +%s)

# Create A record to ALB
aws route53 change-resource-record-sets --hosted-zone-id YOUR_ZONE_ID --change-batch file://dns-change.json
```

### SSL Certificate with ACM

```bash
# Request certificate
aws acm request-certificate \
  --domain-name prompts.yourcompany.com \
  --validation-method DNS

# Add HTTPS listener to ALB
aws elbv2 create-listener \
  --load-balancer-arn YOUR_ALB_ARN \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=YOUR_CERT_ARN \
  --default-actions Type=forward,TargetGroupArn=YOUR_TG_ARN
```

## Monitoring and Logging

### CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/prompt-library

# View logs
aws logs tail /ecs/prompt-library --follow
```

### CloudWatch Alarms

```bash
# Create CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name prompt-library-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

## Auto-Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/prompt-library-cluster/prompt-library-service \
  --min-capacity 1 \
  --max-capacity 4

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/prompt-library-cluster/prompt-library-service \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

## Cost Optimization Tips

1. **Use AWS Lightsail** for simple deployments ($7/month)
2. **Right-size your instances** (start with 0.25 vCPU, 512MB)
3. **Use Fargate Spot** for 70% savings (for non-critical workloads)
4. **Enable CloudWatch Logs insights** instead of third-party tools
5. **Use S3 for database backups** (pennies per month)

## Cleanup

```bash
# Delete Lightsail service
aws lightsail delete-container-service --service-name prompt-library

# Delete ECS service
aws ecs delete-service --cluster prompt-library-cluster --service prompt-library-service --force
aws ecs delete-cluster --cluster prompt-library-cluster

# Delete ECR repository
aws ecr delete-repository --repository-name prompt-library --force
```

## Support

- AWS Documentation: <https://docs.aws.amazon.com/>
- ECS Guide: <https://docs.aws.amazon.com/ecs/>
- Lightsail Guide: <https://lightsail.aws.amazon.com/ls/docs/>
