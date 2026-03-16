# Gate Controller Quick Start Guide

Get your Raspberry Pi gate controller up and running in 5 minutes!

## Prerequisites

- Raspberry Pi with Raspberry Pi OS
- Internet connection
- 2x relay modules (for UP/DN control)
- Momentary push button
- Jumper wires
- Redis server (will be installed automatically)

## Installation (One Command!)

```bash
cd /path/to/gate-controller
sudo ./setup.sh
```

That's it! The setup script will:
- ✅ Install all dependencies (Redis, Python packages)
- ✅ Generate a secure API key
- ✅ Create the service user
- ✅ Install systemd services
- ✅ Configure log rotation
- ✅ Start all services
- ✅ Validate the installation

## After Installation

### 1. Save Your API Key

The setup script displays your API key. Save it!

```bash
# View your key anytime
./gate.sh key
```

### 2. Test the System

```bash
# Check health (no auth needed)
curl http://localhost:8000/health

# Test with API key
./gate.sh test
```

### 3. Check Status

```bash
./gate.sh status
```

## Daily Usage

### Control Gate

```bash
# Using the management script
./gate.sh test
# Then choose option 2 to activate

# Or directly with curl
curl -X POST -H "X-API-Key: YOUR_KEY" http://localhost:8000/gate/activate
```

### View Logs

```bash
./gate.sh logs
```

### Check System Health

```bash
./gate.sh health
```

### Restart Services

```bash
./gate.sh restart
```

## Management Commands

All management is done via the `gate.sh` script:

```bash
./gate.sh status      # Show status of all services
./gate.sh start       # Start all services
./gate.sh stop        # Stop all services
./gate.sh restart     # Restart all services
./gate.sh logs        # View logs
./gate.sh health      # Health check
./gate.sh test        # Test the API
./gate.sh key         # Show API key
./gate.sh stats       # Show Redis stats
./gate.sh help        # Show all commands
```

## Configuration

Edit `gate_control/config.py` to customize:

```python
# Timing
DOOR_TRAVEL_TIME = 9.15  # Seconds for door to fully open/close
PULSE = 0.5              # Seconds to hold relay
CADENCE = 0.05           # Loop check interval

# Button thresholds
SWITCH_THRESHOLD = 0.25  # Short press (< 0.25s = activate)
SWITCH_EBRAKE = 1.5      # Long press (> 1.5s = ebrake)

# Logging
LOG_LEVEL = 0  # 0=verbose, 3=quiet
```

After changing config:
```bash
./gate.sh restart
```

## Hardware Wiring

Connect to these GPIO pins (BOARD numbering):

| Component | Pin | Function |
|-----------|-----|----------|
| UP Relay ON | 33 | Activate UP relay |
| UP Relay OFF | 37 | Deactivate UP relay |
| DN Relay ON | 18 | Activate DOWN relay |
| DN Relay OFF | 12 | Deactivate DOWN relay |
| Button | 32 | Physical button input |

See `readme.md` for detailed wiring diagrams.

## Backup & Restore

### Create Backup

```bash
./backup.sh my_backup_name
```

Backs up:
- Configuration
- API key
- Service files
- Redis state

### Restore Backup

```bash
tar -xzf backups/my_backup_name.tar.gz
cp my_backup_name/config.py gate_control/
cp my_backup_name/.api_key ./
sudo cp my_backup_name/services/*.service /lib/systemd/system/
sudo systemctl daemon-reload
./gate.sh restart
```

## Monitoring

### Manual Check

```bash
python3 monitor.py
```

### Automated Monitoring (Cron)

Add to crontab (`crontab -e`):

```bash
# Check every 5 minutes
*/5 * * * * /home/gate/gate-controller/monitor.py >> /home/gate/logs/monitor.log 2>&1

# Daily backup at 2 AM
0 2 * * * /home/gate/gate-controller/backup.sh daily >> /home/gate/logs/backup.log 2>&1
```

## Troubleshooting

### Services Won't Start

```bash
# Check Redis
sudo systemctl status redis-server

# Check logs
./gate.sh logs

# Validate config
python3 validate_config.py
```

### API Not Responding

```bash
# Check if service is running
sudo systemctl status gate-api

# Check logs
sudo journalctl -u gate-api -n 50

# Test Redis
redis-cli ping
```

### Door Not Moving

1. Check ebrake status: `./gate.sh test` → option 3
2. Check door state: `./gate.sh test` → option 1
3. Check service logs: `./gate.sh logs`
4. Verify GPIO wiring

### Lost API Key

```bash
# View saved key
./gate.sh key

# Or generate new one
python3 generate_api_key.py
# Then update gate_control/config.py
```

## API Reference

### Endpoints

All endpoints require API key (except `/health`):

**Health Check**
```bash
GET /health
```

**Get Status**
```bash
GET /gate/status
```

**Activate Gate**
```bash
POST /gate/activate
```

**Emergency Brake**
```bash
GET /gate/ebrake   # Get status
POST /gate/ebrake  # Toggle
```

### Authentication

Include API key in one of two ways:

1. **Header** (recommended):
```bash
curl -H "X-API-Key: YOUR_KEY" http://localhost:8000/gate/status
```

2. **Query Parameter**:
```bash
curl "http://localhost:8000/gate/status?api_key=YOUR_KEY"
```

## Remote Access (Optional)

### Option 1: SSH Tunnel (Safest)

From your local machine:
```bash
ssh -L 8000:localhost:8000 gate@raspberry-pi-ip
```

Then access: `http://localhost:8000`

### Option 2: VPN

Connect to your home VPN, then access: `http://raspberry-pi-ip:8000`

### Option 3: Reverse Proxy with HTTPS (Advanced)

Use nginx + Let's Encrypt:

```nginx
server {
    listen 443 ssl;
    server_name gate.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/gate.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gate.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Uninstall

```bash
sudo ./uninstall.sh
```

This stops services but keeps your project files.

## Getting Help

1. Check logs: `./gate.sh logs`
2. Run validation: `python3 validate_config.py`
3. Check service status: `./gate.sh status`
4. Read full docs: `readme.md`
5. Review improvements: `IMPROVEMENTS.md`

## Next Steps

- Set up automated backups (cron job)
- Set up monitoring alerts
- Integrate with home automation (Home Assistant, etc.)
- Build a mobile app using the API
- Add additional sensors (reed switches, etc.)

---

**Quick Reference:**

| Task | Command |
|------|---------|
| Install | `sudo ./setup.sh` |
| Check status | `./gate.sh status` |
| View logs | `./gate.sh logs` |
| Test API | `./gate.sh test` |
| Show API key | `./gate.sh key` |
| Restart services | `./gate.sh restart` |
| Create backup | `./backup.sh` |
| Validate config | `python3 validate_config.py` |
| Monitor system | `python3 monitor.py` |
| Uninstall | `sudo ./uninstall.sh` |
