#!/bin/bash

#######################################################################
# Gate Controller Uninstall Script
# 
# This script removes the gate controller from your system
# Run with: sudo ./uninstall.sh
#######################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}$1${NC}"
    echo -e "${RED}========================================${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root: sudo ./uninstall.sh"
    exit 1
fi

print_header "Gate Controller Uninstall"

echo ""
print_warning "This will:"
echo "  - Stop all gate controller services"
echo "  - Remove systemd service files"
echo "  - Keep your project files and configuration"
echo "  - Keep Redis installed"
echo "  - Keep the 'gate' user account"
echo ""

read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Uninstall cancelled"
    exit 0
fi

echo ""

# Stop services
print_info "Stopping services..."
for service in doorman gate-api button-sense; do
    systemctl stop "$service.service" 2>/dev/null || true
    systemctl disable "$service.service" 2>/dev/null || true
done
print_success "Services stopped and disabled"

# Remove systemd service files
print_info "Removing systemd service files..."
for service in doorman gate-api button-sense; do
    rm -f "/lib/systemd/system/$service.service"
done
systemctl daemon-reload
print_success "Service files removed"

# Remove log rotation config
print_info "Removing log rotation configuration..."
rm -f /etc/logrotate.d/gate-controller
print_success "Log rotation removed"

echo ""
print_header "Uninstall Complete"
echo ""
print_success "Gate controller has been removed from your system"
echo ""
echo "Your project files are still in: $(pwd)"
echo "To completely remove, run: rm -rf $(pwd)"
echo ""
echo "Redis is still installed. To remove: sudo apt-get remove redis-server"
echo ""
