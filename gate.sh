#!/bin/bash

#######################################################################
# Gate Controller Management Script
# 
# Easy management commands for the gate controller
# Usage: ./gate.sh [command]
#######################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if .api_key file exists
get_api_key() {
    if [ -f "$SCRIPT_DIR/.api_key" ]; then
        cat "$SCRIPT_DIR/.api_key" | cut -d= -f2
    else
        echo "NOT_SET"
    fi
}

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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Show help
show_help() {
    echo ""
    echo "Gate Controller Management"
    echo ""
    echo "Usage: ./gate.sh [command]"
    echo ""
    echo "Commands:"
    echo "  status      Show status of all services"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  logs        Show logs from all services"
    echo "  health      Check API health"
    echo "  test        Test the API with your key"
    echo "  key         Show your API key"
    echo "  stats       Show Redis stats"
    echo "  help        Show this help message"
    echo ""
}

# Check service status
check_status() {
    print_header "Service Status"
    
    for service in doorman gate-api button-sense; do
        if systemctl is-active --quiet "$service.service"; then
            status="${GREEN}● Running${NC}"
        else
            status="${RED}○ Stopped${NC}"
        fi
        echo -e "$service: $status"
    done
    
    echo ""
    
    # Quick health check
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        print_success "API is healthy"
    else
        print_error "API is not responding"
    fi
    
    echo ""
}

# Start services
start_services() {
    print_header "Starting Services"
    
    for service in doorman gate-api button-sense; do
        print_info "Starting $service..."
        sudo systemctl start "$service.service"
    done
    
    sleep 2
    check_status
}

# Stop services
stop_services() {
    print_header "Stopping Services"
    
    for service in doorman gate-api button-sense; do
        print_info "Stopping $service..."
        sudo systemctl stop "$service.service"
    done
    
    echo ""
    print_success "All services stopped"
    echo ""
}

# Restart services
restart_services() {
    print_header "Restarting Services"
    
    for service in doorman gate-api button-sense; do
        print_info "Restarting $service..."
        sudo systemctl restart "$service.service"
    done
    
    sleep 2
    check_status
}

# Show logs
show_logs() {
    print_header "Service Logs (Ctrl+C to exit)"
    echo ""
    
    echo "Choose which logs to view:"
    echo "  1) doorman"
    echo "  2) gate-api"
    echo "  3) button-sense"
    echo "  4) all services"
    echo "  5) application logs (~/logs/*.txt)"
    echo ""
    read -p "Enter choice [1-5]: " choice
    
    case $choice in
        1) sudo journalctl -u doorman -f ;;
        2) sudo journalctl -u gate-api -f ;;
        3) sudo journalctl -u button-sense -f ;;
        4) sudo journalctl -u doorman -u gate-api -u button-sense -f ;;
        5) tail -f ~/logs/*.txt ;;
        *) print_error "Invalid choice"; exit 1 ;;
    esac
}

# Health check
health_check() {
    print_header "Health Check"
    
    # API health
    print_info "Checking API health..."
    curl -s http://localhost:8000/health | python3 -m json.tool
    
    echo ""
    
    # Redis check
    print_info "Checking Redis..."
    if redis-cli ping | grep -q "PONG"; then
        print_success "Redis is responding"
    else
        print_error "Redis is not responding"
    fi
    
    echo ""
}

# Test API
test_api() {
    API_KEY=$(get_api_key)
    
    if [ "$API_KEY" = "NOT_SET" ]; then
        print_error "API key not found. Run setup.sh first."
        exit 1
    fi
    
    print_header "API Test"
    echo ""
    echo "Choose test:"
    echo "  1) Get gate status"
    echo "  2) Activate gate"
    echo "  3) Get ebrake status"
    echo "  4) Toggle ebrake"
    echo "  5) Health check"
    echo ""
    read -p "Enter choice [1-5]: " choice
    
    echo ""
    
    case $choice in
        1)
            print_info "Getting gate status..."
            curl -s -H "X-API-Key: $API_KEY" http://localhost:8000/gate/status | python3 -m json.tool
            ;;
        2)
            print_info "Activating gate..."
            read -p "Are you sure? (yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                curl -s -X POST -H "X-API-Key: $API_KEY" http://localhost:8000/gate/activate | python3 -m json.tool
            else
                echo "Cancelled"
            fi
            ;;
        3)
            print_info "Getting ebrake status..."
            curl -s -H "X-API-Key: $API_KEY" http://localhost:8000/gate/ebrake | python3 -m json.tool
            ;;
        4)
            print_info "Toggling ebrake..."
            curl -s -X POST -H "X-API-Key: $API_KEY" http://localhost:8000/gate/ebrake | python3 -m json.tool
            ;;
        5)
            health_check
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    echo ""
}

# Show API key
show_key() {
    API_KEY=$(get_api_key)
    
    if [ "$API_KEY" = "NOT_SET" ]; then
        print_error "API key not found. Run setup.sh first."
        exit 1
    fi
    
    print_header "Your API Key"
    echo ""
    echo "$API_KEY"
    echo ""
    echo "Usage examples:"
    echo "  curl -H 'X-API-Key: $API_KEY' http://localhost:8000/gate/status"
    echo ""
}

# Show Redis stats
show_stats() {
    print_header "Redis Statistics"
    
    redis-cli info stats | grep -E "(total_connections|total_commands|keyspace)"
    
    echo ""
    print_info "Door state:"
    redis-cli get state
    echo ""
    print_info "Ebrake status:"
    redis-cli get ebrake
    echo ""
    print_info "Stream length:"
    redis-cli xlen HELMS_DEEP
    echo ""
}

# Main command router
case "${1:-help}" in
    status)
        check_status
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    health)
        health_check
        ;;
    test)
        test_api
        ;;
    key)
        show_key
        ;;
    stats)
        show_stats
        ;;
    help|*)
        show_help
        ;;
esac
