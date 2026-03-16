#!/bin/bash

#######################################################################
# Gate Controller Setup Script
# 
# This script installs and configures the Raspberry Pi Gate Controller
# Run with: sudo ./setup.sh
#######################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root: sudo ./setup.sh"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="gate-controller"

print_header "Gate Controller Setup"
echo ""

#######################################################################
# STEP 1: Check System Requirements
#######################################################################
print_header "Step 1: Checking System Requirements"

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    print_warning "Not running on Raspberry Pi - will use MockGPIO"
    IS_PI=false
else
    print_success "Running on Raspberry Pi"
    cat /proc/device-tree/model
    IS_PI=true
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python $PYTHON_VERSION found"

# Check if systemd is available
if ! command -v systemctl &> /dev/null; then
    print_error "systemd not found"
    exit 1
fi
print_success "systemd available"

echo ""

#######################################################################
# STEP 2: Install System Dependencies
#######################################################################
print_header "Step 2: Installing System Dependencies"

# Update package list
print_info "Updating package list..."
apt-get update -qq

# Install Redis
if ! command -v redis-server &> /dev/null; then
    print_info "Installing Redis server..."
    apt-get install -y redis-server
    print_success "Redis installed"
else
    print_success "Redis already installed"
fi

# Install Python pip
if ! command -v pip3 &> /dev/null; then
    print_info "Installing Python pip..."
    apt-get install -y python3-pip
    print_success "pip installed"
else
    print_success "pip already installed"
fi

# Install Python development headers (needed for some packages)
if [ "$IS_PI" = true ]; then
    print_info "Installing Python development headers..."
    apt-get install -y python3-dev
fi

echo ""

#######################################################################
# STEP 3: Install Python Dependencies
#######################################################################
print_header "Step 3: Installing Python Dependencies"

cd "$SCRIPT_DIR"

if [ -f requirements.txt ]; then
    print_info "Installing Python packages..."
    pip3 install -r requirements.txt
    print_success "Python packages installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

echo ""

#######################################################################
# STEP 4: Configure Redis
#######################################################################
print_header "Step 4: Configuring Redis"

# Enable Redis to start on boot
print_info "Enabling Redis to start on boot..."
systemctl enable redis-server
systemctl start redis-server

# Test Redis connection
if redis-cli ping | grep -q "PONG"; then
    print_success "Redis is running and responding"
else
    print_error "Redis is not responding"
    exit 1
fi

echo ""

#######################################################################
# STEP 5: Generate API Key
#######################################################################
print_header "Step 5: Configuring API Key"

CONFIG_FILE="$SCRIPT_DIR/gate_control/config.py"

# Check if API key is already set
if grep -q "your-secret-api-key-here-change-this" "$CONFIG_FILE" 2>/dev/null; then
    print_info "Generating secure API key..."
    
    # Generate API key
    API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Update config file
    sed -i "s/your-secret-api-key-here-change-this/$API_KEY/" "$CONFIG_FILE"
    
    print_success "API key generated and saved to config.py"
    print_info "Your API key: $API_KEY"
    echo ""
    print_warning "SAVE THIS KEY! You'll need it to access the API"
    echo ""
    echo "API_KEY=$API_KEY" > "$SCRIPT_DIR/.api_key"
    chmod 600 "$SCRIPT_DIR/.api_key"
    print_info "API key also saved to .api_key file (kept private)"
else
    print_success "API key already configured"
fi

echo ""

#######################################################################
# STEP 6: Validate Configuration
#######################################################################
print_header "Step 6: Validating Configuration"

cd "$SCRIPT_DIR"
if python3 validate_config.py; then
    print_success "Configuration validated successfully"
else
    print_warning "Configuration validation failed - check warnings above"
fi

echo ""

#######################################################################
# STEP 7: Create Service User (if needed)
#######################################################################
print_header "Step 7: Setting Up Service User"

SERVICE_USER="gate"

if id "$SERVICE_USER" &>/dev/null; then
    print_success "User '$SERVICE_USER' already exists"
else
    print_info "Creating user '$SERVICE_USER'..."
    useradd -r -s /bin/false "$SERVICE_USER"
    print_success "User created"
fi

# Set ownership of project directory
print_info "Setting ownership of project files..."
chown -R "$SERVICE_USER:$SERVICE_USER" "$SCRIPT_DIR"
print_success "Ownership set"

# Add gate user to gpio group (for GPIO access)
if [ "$IS_PI" = true ]; then
    if getent group gpio > /dev/null 2>&1; then
        print_info "Adding user to gpio group..."
        usermod -a -G gpio "$SERVICE_USER"
        print_success "User added to gpio group"
    fi
fi

echo ""

#######################################################################
# STEP 8: Install Systemd Services
#######################################################################
print_header "Step 8: Installing Systemd Services"

# Update service files with correct path
print_info "Updating service files with project path..."

for service_file in doorman.service gate-api.service button-sense.service; do
    if [ -f "$SCRIPT_DIR/$service_file" ]; then
        # Update WorkingDirectory
        sed -i "s|WorkingDirectory=.*|WorkingDirectory=$SCRIPT_DIR|" "$SCRIPT_DIR/$service_file"
        # Update ExecStart path
        sed -i "s|ExecStart=.*$SCRIPT_DIR|ExecStart=$SCRIPT_DIR|" "$SCRIPT_DIR/$service_file"
        
        # Copy to systemd directory
        cp "$SCRIPT_DIR/$service_file" /lib/systemd/system/
        print_success "$service_file installed"
    else
        print_warning "$service_file not found"
    fi
done

# Reload systemd
print_info "Reloading systemd daemon..."
systemctl daemon-reload
print_success "Systemd reloaded"

# Enable services to start on boot
print_info "Enabling services to start on boot..."
systemctl enable doorman.service
systemctl enable gate-api.service
systemctl enable button-sense.service
print_success "Services enabled"

echo ""

#######################################################################
# STEP 9: Set Up Log Rotation
#######################################################################
print_header "Step 9: Setting Up Log Rotation"

LOGROTATE_CONF="/etc/logrotate.d/gate-controller"

cat > "$LOGROTATE_CONF" <<EOF
/home/gate/logs/*.txt {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 gate gate
}
EOF

print_success "Log rotation configured"
echo ""

#######################################################################
# STEP 10: Start Services
#######################################################################
print_header "Step 10: Starting Services"

print_info "Starting doorman..."
systemctl start doorman.service
sleep 1

print_info "Starting gate-api..."
systemctl start gate-api.service
sleep 1

print_info "Starting button-sense..."
systemctl start button-sense.service
sleep 1

echo ""

#######################################################################
# STEP 11: Verify Installation
#######################################################################
print_header "Step 11: Verifying Installation"

# Check service status
SERVICES_RUNNING=true

for service in doorman gate-api button-sense; do
    if systemctl is-active --quiet "$service.service"; then
        print_success "$service.service is running"
    else
        print_error "$service.service is not running"
        SERVICES_RUNNING=false
    fi
done

echo ""

# Test API health endpoint
print_info "Testing API health endpoint..."
sleep 2  # Give API time to fully start

if curl -s http://localhost:8000/health | grep -q "healthy"; then
    print_success "API health check passed"
else
    print_warning "API health check failed (service may still be starting)"
fi

echo ""

#######################################################################
# Final Summary
#######################################################################
print_header "Installation Complete!"

echo ""
echo -e "${GREEN}Your Gate Controller is now installed and running!${NC}"
echo ""

# Get API key if available
if [ -f "$SCRIPT_DIR/.api_key" ]; then
    API_KEY=$(cat "$SCRIPT_DIR/.api_key" | cut -d= -f2)
    
    echo -e "${YELLOW}Your API Key:${NC} $API_KEY"
    echo ""
    echo -e "${YELLOW}Quick Test Commands:${NC}"
    echo "  # Health check (no auth needed)"
    echo "  curl http://localhost:8000/health"
    echo ""
    echo "  # Get gate status"
    echo "  curl -H 'X-API-Key: $API_KEY' http://localhost:8000/gate/status"
    echo ""
    echo "  # Activate gate"
    echo "  curl -X POST -H 'X-API-Key: $API_KEY' http://localhost:8000/gate/activate"
    echo ""
fi

echo -e "${YELLOW}Useful Commands:${NC}"
echo "  Check service status:"
echo "    sudo systemctl status doorman gate-api button-sense"
echo ""
echo "  View logs:"
echo "    sudo journalctl -u doorman -f"
echo "    tail -f ~/logs/*.txt"
echo ""
echo "  Restart services:"
echo "    sudo systemctl restart doorman gate-api button-sense"
echo ""
echo "  Stop services:"
echo "    sudo systemctl stop doorman gate-api button-sense"
echo ""

echo -e "${YELLOW}Configuration:${NC}"
echo "  Config file: $SCRIPT_DIR/gate_control/config.py"
echo "  API key file: $SCRIPT_DIR/.api_key"
echo "  Documentation: $SCRIPT_DIR/readme.md"
echo ""

echo -e "${GREEN}Happy gating! 🚗🔧${NC}"
