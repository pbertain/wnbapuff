# SportsPuff Ansible Deployment

This directory contains the Ansible deployment configuration for the SportsPuff Multi-Sport API Server.

## Overview

The deployment uses Ansible to automate the installation and configuration of:
- Python virtual environment with dependencies
- Systemd service for the API server
- Nginx reverse proxy configuration
- SSL/TLS support (optional)

## Files

- `playbook.yml` - Main Ansible playbook
- `inventory.yml` - Server inventory configuration
- `deployment.env` - Deployment environment variables
- `vars/main.yml` - Ansible variables
- `templates/` - Configuration templates
  - `sportspuff-api.service.j2` - Systemd service template
  - `nginx.conf.j2` - Nginx configuration template
  - `environment.j2` - Environment variables template
- `deploy.sh` - Deployment script
- `check-status.sh` - Status check script

## Configuration

### 1. Update deployment.env

Edit `deployment.env` with your configuration:

```bash
# Host configurations
SPORTSPUFF_HOST_1=your-server-1.com
SPORTSPUFF_HOST_2=your-server-2.com

# API Keys
WNBA_SPORTSBLAZE_KEY=your_sportsblaze_key
WNBA_RAPIDAPI_KEY=your_rapidapi_key
```

### 2. Update inventory.yml

Modify the hosts in `inventory.yml` to match your servers.

### 3. SSL Configuration (Optional)

To enable SSL, set these environment variables:
```bash
export NGINX_SSL_CERT=/path/to/cert.pem
export NGINX_SSL_KEY=/path/to/key.pem
export NGINX_SERVER_NAME=your-domain.com
```

## Deployment

### Quick Deploy

```bash
cd ansible
./deploy.sh
```

### Manual Deploy

```bash
cd ansible
ansible-playbook -i inventory.yml playbook.yml --ask-become-pass
```

## Status Check

```bash
cd ansible
./check-status.sh
```

## Ports

- **34080**: FastAPI (main JSON API) - proxied by nginx
- **34081**: Flask (human-readable endpoints) - local access only

## Services

- `sportspuff-api`: Main API service
- `nginx`: Reverse proxy

## API Endpoints

After deployment, the API will be available at:

- **JSON API**: `https://your-domain.com/api/`
- **Human-readable**: `http://your-server:34081/curl/`

## Troubleshooting

### Check Service Status
```bash
systemctl status sportspuff-api
systemctl status nginx
```

### View Logs
```bash
journalctl -u sportspuff-api -f
tail -f /var/log/nginx/error.log
```

### Test API
```bash
curl http://localhost:34080/api/wnba/standings
curl http://localhost:34081/curl/wnba/help
``` 