## pi-gate

A Raspberry Pi garage door controller for my 50+ year old garage door.

### Services

- **Button Watcher** (`button_sense.py`): Watches the door buttons continuously and sends messages to the door controller.
  - Short press (< 0.25s): Activate door
  - Long press (> 1.5s): Toggle emergency brake
  
- **API** (`gate_api.py`): REST API for remote control and monitoring.
  - Port: 8000 (via gunicorn)
  - Requires API key authentication
  
- **Door Controller** (`doorman.py`): Controls the relays used to operate the door.
  - Manages UP/DN relays
  - Handles door travel time
  - Processes events from Redis stream

### Architecture

All services communicate via Redis Streams:
- Events are published to `HELMS_DEEP` stream
- Processed events are tracked in `HD_Handled` list
- Door state stored in Redis keys: `state`, `ebrake`, `t`

### Quick Start

1. **Install dependencies**:
   ```bash
   sudo apt-get install redis-server python3-pip
   pip3 install -r requirements.txt
   ```

2. **Generate API key**:
   ```bash
   python3 generate_api_key.py
   # Copy the generated key to gate_control/config.py
   ```

3. **Validate configuration**:
   ```bash
   python3 validate_config.py
   ```

4. **Install systemd services**:
   ```bash
   sudo ./install
   ```

5. **Start services**:
   ```bash
   sudo systemctl start doorman
   sudo systemctl start gate-api
   sudo systemctl start button-sense
   ```

### API Documentation

#### Authentication

All endpoints (except `/health`) require an API key via:
- HTTP Header: `X-API-Key: your-api-key`
- Query Parameter: `?api_key=your-api-key`

#### Endpoints

**Health Check** (no auth required)
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "redis": "ok",
  "timestamp": 1234567890.123
}
```

**Activate Gate**
```bash
POST /gate/activate
```
Response:
```json
{
  "state": "Opening",
  "message": "Gate activation initiated"
}
```

**Get Gate Status**
```bash
GET /gate/status
```
Response:
```json
{
  "state": "DN",
  "ebrake": "0"
}
```

**Emergency Brake**
```bash
GET /gate/ebrake    # Get ebrake status
POST /gate/ebrake   # Toggle ebrake
```
Response:
```json
{
  "ebrake": "1"
}
```

#### Example Usage

```bash
# Set your API key
API_KEY="your-api-key-here"

# Check health
curl http://localhost:8000/health

# Get status
curl -H "X-API-Key: $API_KEY" http://localhost:8000/gate/status

# Activate gate
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:8000/gate/activate

# Toggle ebrake
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:8000/gate/ebrake
```

### Configuration

Edit `gate_control/config.py` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `API_KEY` | REST API authentication key | *must be set* |
| `DOOR_TRAVEL_TIME` | Time for door to fully open/close (seconds) | 9.15 |
| `PULSE` | Relay activation duration (seconds) | 0.5 |
| `CADENCE` | Main loop sleep time (seconds) | 0.05 |
| `SWITCH_EBRAKE` | Long press threshold for ebrake (seconds) | 1.5 |
| `SWITCH_THRESHOLD` | Short press threshold (seconds) | 0.25 |
| `LOG_LEVEL` | Logging verbosity (0=most, 3=least) | 0 |

### GPIO Pin Assignments

| Component | GPIO Pin (BOARD) | Function |
|-----------|------------------|----------|
| UP Relay ON | 33 | Activate UP relay |
| UP Relay OFF | 37 | Deactivate UP relay |
| DN Relay ON | 18 | Activate DOWN relay |
| DN Relay OFF | 12 | Deactivate DOWN relay |
| Button Sensor | 32 | Physical button input |

### Monitoring

Check service status:
```bash
sudo systemctl status doorman
sudo systemctl status gate-api
sudo systemctl status button-sense
```

View logs:
```bash
# Service logs
sudo journalctl -u doorman -f
sudo journalctl -u gate-api -f
sudo journalctl -u button-sense -f

# Application logs
tail -f ~/logs/*.txt
```

### Safety Features

- **Emergency Brake (ebrake)**: Disables all door operations until cleared
  - Long press physical button (> 1.5s)
  - POST to `/gate/ebrake` endpoint
  
- **Door Travel Time**: Prevents relays from running too long
  
- **Interrupt Capability**: Stops current operation if new command received

### Troubleshooting

**API returns 401/403**: 
- Verify API_KEY is set correctly in config.py
- Check you're sending the API key in header or query param

**Services won't start**:
- Check Redis is running: `sudo systemctl status redis-server`
- Validate config: `python3 validate_config.py`
- Check logs: `sudo journalctl -u <service-name> -n 50`

**GPIO not working**:
- Ensure running on Raspberry Pi (not dev machine)
- Check GPIO pins are not in use by other services
- Verify relay wiring

**Door won't move**:
- Check ebrake status: `curl http://localhost:8000/gate/ebrake`
- Verify door state: `curl -H "X-API-Key: $API_KEY" http://localhost:8000/gate/status`
- Check doorman service logs

### Development

Running without Raspberry Pi hardware:
- MockGPIO is automatically used when RPi.GPIO is unavailable
- All services will run but relays won't actually trigger

Running tests:
```bash
cd gate_control/tests
python3 doorman.py
```

### Hardware Requirements

- Raspberry Pi (any model with GPIO)
- 2x Relay modules (for UP/DN control)
- Momentary push button
- Jumper wires
- Redis server

---

Project Details: https://www.glue-and-screw.com/projects/gate
