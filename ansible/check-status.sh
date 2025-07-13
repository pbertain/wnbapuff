#!/bin/bash

# Sportspuff Status Check Script
# This script checks the status of the Sportspuff Multi-Sport API Server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Check if we're in the ansible directory
if [ ! -f "playbook.yml" ]; then
    print_error "This script must be run from the ansible directory"
    exit 1
fi

# Load environment variables
if [ -f "deployment.env" ]; then
    source deployment.env
else
    print_warning "deployment.env not found, using default values"
fi

print_header "Sportspuff Status Check"
echo "================================"

# Check service status on all hosts
print_status "Checking service status on all hosts..."
ansible sportspuff_servers -i inventory.yml -m systemd -a "name=sportspuff-api state=started" --ask-become-pass

# Check nginx status
print_status "Checking nginx status..."
ansible sportspuff_servers -i inventory.yml -m systemd -a "name=nginx state=started" --ask-become-pass

# Check if ports are listening
print_status "Checking if ports are listening..."
ansible sportspuff_servers -i inventory.yml -m shell -a "netstat -tlnp | grep -E ':(34080|34081)'" --ask-become-pass

# Test API endpoints
print_status "Testing API endpoints..."
ansible sportspuff_servers -i inventory.yml -m uri -a "url=http://localhost:34080/api/wnba/standings method=GET" --ask-become-pass

print_status "Status check completed!" 