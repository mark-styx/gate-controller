#!/bin/bash

#######################################################################
# Gate Controller Backup Script
# 
# Creates a backup of configuration and state
# Usage: ./backup.sh [backup_name]
#######################################################################

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="${1:-backup_$TIMESTAMP}"

echo -e "${BLUE}Creating backup: $BACKUP_NAME${NC}"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Backup configuration
echo "Backing up configuration..."
cp "$SCRIPT_DIR/gate_control/config.py" "$BACKUP_DIR/$BACKUP_NAME/"
echo -e "${GREEN}✓ Configuration backed up${NC}"

# Backup API key
if [ -f "$SCRIPT_DIR/.api_key" ]; then
    cp "$SCRIPT_DIR/.api_key" "$BACKUP_DIR/$BACKUP_NAME/"
    echo -e "${GREEN}✓ API key backed up${NC}"
fi

# Backup systemd service files
echo "Backing up service files..."
mkdir -p "$BACKUP_DIR/$BACKUP_NAME/services"
cp "$SCRIPT_DIR"/*.service "$BACKUP_DIR/$BACKUP_NAME/services/" 2>/dev/null || true
echo -e "${GREEN}✓ Service files backed up${NC}"

# Backup Redis state
echo "Backing up Redis state..."
redis-cli get state > "$BACKUP_DIR/$BACKUP_NAME/redis_state.txt" 2>/dev/null || true
redis-cli get ebrake >> "$BACKUP_DIR/$BACKUP_NAME/redis_state.txt" 2>/dev/null || true
redis-cli get t >> "$BACKUP_DIR/$BACKUP_NAME/redis_state.txt" 2>/dev/null || true
echo -e "${GREEN}✓ Redis state backed up${NC}"

# Create README for backup
cat > "$BACKUP_DIR/$BACKUP_NAME/README.txt" <<EOF
Gate Controller Backup: $BACKUP_NAME
Created: $(date)
================================

Contents:
- config.py: Configuration file
- .api_key: API key file (if exists)
- services/: Systemd service files
- redis_state.txt: Redis state snapshot

To restore:
1. Copy config.py to gate_control/
2. Copy .api_key to project root (if needed)
3. Copy service files to /lib/systemd/system/
4. Restart services: sudo systemctl restart doorman gate-api button-sense
5. Redis state is informational only (not restored)
EOF

# Compress backup
echo "Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"

echo ""
echo -e "${GREEN}✓ Backup created: $BACKUP_DIR/$BACKUP_NAME.tar.gz${NC}"
echo ""

# Clean old backups (keep last 10)
echo "Cleaning old backups (keeping last 10)..."
ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true

echo -e "${GREEN}✓ Done!${NC}"
echo ""
echo "To restore: tar -xzf $BACKUP_DIR/$BACKUP_NAME.tar.gz"
