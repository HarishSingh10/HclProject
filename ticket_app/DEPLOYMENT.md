# 🚀 Deployment Guide

Complete guide for deploying the IT Support Assistant to production.

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud](#streamlit-cloud)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Heroku Deployment](#heroku-deployment)
6. [Production Checklist](#production-checklist)

---

## Local Development

### Quick Start
```bash
# Clone/navigate to project
cd ticket_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Development Server
- URL: `http://localhost:8501`
- Auto-reload on file changes
- Debug mode enabled

---

## Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- Code pushed to GitHub

### Deployment Steps

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repository
   - Select branch and main file: `app.py`

3. **Configure Secrets:**
   - In Streamlit Cloud dashboard
   - Go to "Settings" → "Secrets"
   - Add your secrets:
   ```toml
   backend_url = "https://your-api.example.com"
   ```

4. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - App is live!

### Environment Variables
Set in Streamlit Cloud dashboard:
```toml
backend_url = "https://api.example.com"
```

### Custom Domain
1. Go to app settings
2. Add custom domain
3. Update DNS records
4. Verify domain

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "8501:8501"
    environment:
      - backend_url=http://backend:8000
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    image: your-backend-image:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/tickets
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=tickets
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Build and Run

```bash
# Build image
docker build -t ticket-app:latest .

# Run container
docker run -p 8501:8501 \
  -e backend_url=http://localhost:8000 \
  ticket-app:latest

# Or use docker-compose
docker-compose up -d
```

### Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag ticket-app:latest username/ticket-app:latest

# Push
docker push username/ticket-app:latest
```

---

## AWS Deployment

### Option 1: AWS App Runner

1. **Push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
   
   docker tag ticket-app:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ticket-app:latest
   
   docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ticket-app:latest
   ```

2. **Create App Runner Service:**
   - Go to AWS App Runner
   - Create new service
   - Select ECR image
   - Configure environment variables
   - Deploy

### Option 2: AWS ECS

1. **Create ECS Cluster:**
   ```bash
   aws ecs create-cluster --cluster-name ticket-app
   ```

2. **Register Task Definition:**
   ```bash
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   ```

3. **Create Service:**
   ```bash
   aws ecs create-service --cluster ticket-app --service-name ticket-app-service --task-definition ticket-app --desired-count 1
   ```

### Option 3: AWS Elastic Beanstalk

1. **Create `.ebextensions/streamlit.config`:**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app:app
     aws:elasticbeanstalk:application:environment:
       PYTHONUNBUFFERED: 1
   ```

2. **Deploy:**
   ```bash
   eb init -p python-3.9 ticket-app
   eb create ticket-app-env
   eb deploy
   ```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deployment Steps

1. **Create Procfile:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create runtime.txt:**
   ```
   python-3.9.16
   ```

3. **Initialize Heroku:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set backend_url=https://your-api.example.com
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **View Logs:**
   ```bash
   heroku logs --tail
   ```

### Heroku Buildpacks
```bash
heroku buildpacks:add heroku/python
```

---

## Production Checklist

### Security
- [ ] Use HTTPS only
- [ ] Set strong secrets
- [ ] Enable CORS properly
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable authentication
- [ ] Use secure headers
- [ ] Regular security audits
- [ ] Keep dependencies updated

### Performance
- [ ] Enable caching
- [ ] Optimize API calls
- [ ] Use CDN for static files
- [ ] Monitor response times
- [ ] Set up load balancing
- [ ] Use database indexing
- [ ] Implement pagination
- [ ] Monitor memory usage

### Monitoring & Logging
- [ ] Set up error tracking (Sentry)
- [ ] Enable application logging
- [ ] Monitor uptime
- [ ] Track user analytics
- [ ] Set up alerts
- [ ] Monitor API performance
- [ ] Track error rates
- [ ] Monitor resource usage

### Backup & Recovery
- [ ] Regular database backups
- [ ] Test backup restoration
- [ ] Document recovery procedures
- [ ] Version control all code
- [ ] Document deployment process
- [ ] Have rollback plan
- [ ] Test disaster recovery

### Configuration
- [ ] Update backend URL
- [ ] Configure CORS
- [ ] Set up SSL/TLS
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure alerts
- [ ] Set up auto-scaling
- [ ] Configure CDN

---

## Environment Variables

### Required
```
backend_url=https://api.example.com
```

### Optional
```
LOG_LEVEL=info
DEBUG=false
CACHE_TTL=300
MAX_UPLOAD_SIZE=200
```

---

## Monitoring & Logging

### Sentry Integration

1. **Install Sentry:**
   ```bash
   pip install sentry-sdk
   ```

2. **Add to app.py:**
   ```python
   import sentry_sdk
   
   sentry_sdk.init(
       dsn="https://your-sentry-dsn@sentry.io/project-id",
       traces_sample_rate=1.0
   )
   ```

### CloudWatch Logs (AWS)

```python
import logging
import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

### Application Performance Monitoring

- **New Relic:** Add `newrelic.ini` and set `NEW_RELIC_CONFIG_FILE`
- **DataDog:** Install `datadog` agent
- **Prometheus:** Export metrics endpoint

---

## Scaling

### Horizontal Scaling
- Use load balancer (AWS ALB, Nginx)
- Deploy multiple instances
- Use session store (Redis)
- Implement sticky sessions

### Vertical Scaling
- Increase instance size
- Increase memory allocation
- Increase CPU allocation

### Database Scaling
- Use read replicas
- Implement caching layer (Redis)
- Optimize queries
- Use connection pooling

---

## Troubleshooting

### App Won't Start
```bash
# Check logs
heroku logs --tail
docker logs container-id

# Check configuration
echo $backend_url
```

### High Memory Usage
- Check for memory leaks
- Implement caching
- Optimize data structures
- Monitor with profiler

### Slow Performance
- Check API response times
- Monitor database queries
- Check network latency
- Review application logs

### Connection Issues
- Verify backend URL
- Check firewall rules
- Verify CORS configuration
- Check network connectivity

---

## Cost Optimization

### Streamlit Cloud
- Free tier available
- Pay-as-you-go for premium
- No infrastructure costs

### Docker/Heroku
- Use free tier if available
- Optimize image size
- Use spot instances (AWS)
- Set up auto-scaling

### AWS
- Use free tier
- Use spot instances
- Implement auto-scaling
- Monitor costs with Cost Explorer

---

## Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Monitor performance daily
- [ ] Backup database daily
- [ ] Security patches immediately
- [ ] Test disaster recovery quarterly

### Update Process
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Test locally
streamlit run app.py

# Deploy
git push heroku main
```

---

## Support & Resources

- Streamlit Docs: https://docs.streamlit.io/deploy
- Docker Docs: https://docs.docker.com
- Heroku Docs: https://devcenter.heroku.com
- AWS Docs: https://docs.aws.amazon.com

---

**Last Updated:** February 23, 2024
