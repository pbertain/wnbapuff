#!/bin/bash

# Sportspuff Deployment Script
# This script deploys the Sportspuff Multi-Sport API Server using Ansible

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the ansible directory
if [ ! -f "playbook.yml" ]; then
    print_error "This script must be run from the ansible directory"
    exit 1
fi

# Check if deployment.env exists
if [ ! -f "deployment.env" ]; then
    print_error "deployment.env file not found. Please create it with your configuration."
    exit 1
fi

# Load environment variables
source deployment.env

print_status "Starting Sportspuff deployment..."

# Run Ansible playbook
print_status "Running Ansible playbook..."
ansible-playbook -i inventory.yml playbook.yml --ask-become-pass

print_status "Deployment completed successfully!"
print_status "Sportspuff API should now be running on your servers."
print_status "Check the service status with: systemctl status sportspuff-api" 