# Gate Controller Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### To Add
- pytest framework with unit tests
- Type hints for better IDE support
- Docstrings for all public functions
- Web dashboard for monitoring
- Contributing guidelines

## [2.0.0] - 2026-03-16

### 🎉 Major Release - Complete Overhaul

This release transforms the gate controller from a personal project into a production-ready, easy-to-install system.

### ✨ Added - Setup & Installation

#### One-Command Installation
- **setup.sh** - Complete automated installation script
  - Installs all system dependencies (Redis, Python packages)
  - Generates secure API key automatically
  - Creates dedicated service user with proper permissions
  - Installs systemd services
  - Configures log rotation
  - Validates the entire installation
  - Color-coded output with progress tracking

#### Easy Management
- **gate.sh** - Management CLI for daily operations
  - `status` - Check all services at a glance
  - `start/stop/restart` - Control services easily
  - `logs` - View logs with interactive menu
  - `health` - Quick health check
  - `test` - Interactive API testing
  - `key` - Display API key
  - `stats` - Redis statistics
  - `help` - Command reference

#### Backup & Restore
- **backup.sh** - Automated backup system
  - Backs up configuration, API key, service files
  - Compresses backups automatically
  - Keeps last 10 backups
  - One-command restore

#### Monitoring
- **monitor.py** - Health monitoring script
  - Checks Redis, API, and all services
  - Validates door state and ebrake status
  - Detects stuck door conditions
  - JSON output for integration
  - Alert system support
  - Can run as cron job

- **alert.sh** - Example alert script
  - Support for multiple notification methods
  - Email, Slack, Discord, Telegram, SMS, webhooks
  - Easy to customize

#### Validation & Utilities
- **validate_config.py** - Configuration validator
  - Checks API key, Redis, GPIO, config values
  - Provides actionable error messages
  - Run before starting services

- **generate_api_key.py** - Secure key generator
  - Cryptographically secure 32-byte keys
  - Shows usage examples
  - Saves to file for easy reference

- **api_example.py** - Integration example
  - Python client class for API
  - Demonstrates all endpoints
  - Ready to use in integrations

- **uninstall.sh** - Clean removal script
  - Stops and removes services
  - Preserves project files
  - Safe and complete

### 🔒 Security Improvements

#### API Authentication
- **Mandatory API keys** for all endpoints (except /health)
- Support for header (`X-API-Key`) authentication
- Support for query parameter (`?api_key=`) authentication
- Generated keys use cryptographically secure random bytes

#### Input Validation
- Type checking for all request parameters
- Proper JSON validation
- Clear error messages for invalid requests

### 🐛 Bug Fixes

#### Critical Bug Fixes
- **Events.py** - Fixed `raise('Invalid Action')` bug
  - Changed to proper exception: `raise ValueError(...)`
  - Added informative error messages with available options

- **doorman.py** - Fixed bare except clauses
  - Replaced `except: pass` with specific exception handling
  - Added comprehensive error logging
  - Proper handling of Redis errors

#### Error Handling
- **Redis connection resilience** 
  - Added retry logic with multiple attempts
  - Connection testing before operations
  - Clear error messages when Redis unavailable
  - Graceful degradation

- **doorman.py control flow**
  - Added try/except around `set_state()` calls
  - Added try/except around `stream_event()` calls
  - Proper error logging throughout

- **gate_api.py**
  - Comprehensive error handling for all endpoints
  - Proper HTTP status codes (400, 401, 403, 404, 500)
  - JSON error responses

### 📊 Reliability Improvements

#### Health Monitoring
- **New `/health` endpoint** (no auth required)
  - Returns system health status
  - Checks Redis connectivity
  - Includes timestamp

#### Better Error Reporting
- All errors logged to `~/logs/*.txt`
- Errors include context for debugging
- User-friendly error messages
- Proper HTTP status codes

#### Service Management
- Services restart on failure (already existed)
- Health checks via gate.sh
- Easy log access

### 📝 Documentation

#### Comprehensive README
- Architecture overview with diagram
- Full API documentation with examples
- Configuration reference table
- GPIO pin assignments
- Monitoring commands
- Safety features
- Troubleshooting guide
- Hardware requirements
- Remote access options

#### New Documentation Files
- **QUICKSTART.md** - 5-minute setup guide
  - Prerequisites
  - One-command installation
  - Post-install steps
  - Daily usage
  - All management commands
  - Backup & restore
  - Monitoring setup
  - Troubleshooting
  - API reference
  - Remote access

- **IMPROVEMENTS.md** - Complete change log
  - All security improvements
  - All bug fixes
  - All reliability improvements
  - Files modified/created
  - Usage instructions
  - Migration notes

- **requirements.txt** - Python dependencies
  - redis
  - flask
  - gunicorn
  - RPi.GPIO

### 💻 Code Quality

#### API Improvements
- All responses return proper JSON
- Consistent error format
- Decorator-based authentication
- Decorator-based validation
- Better code organization

#### Error Messages
- More descriptive throughout
- Include context for debugging
- User-friendly for API consumers

### 🔄 Changed

#### Breaking Changes
- **API now requires authentication**
  - Update any existing scripts to include API key
  - Use header: `X-API-Key: your-key`
  - Or query param: `?api_key=your-key`

#### Non-Breaking Changes
- All existing functionality preserved
- GPIO pins unchanged
- Redis keys unchanged
- Service names unchanged
- Event stream names unchanged

### 📦 Dependencies
- Added requirements.txt with:
  - redis>=4.0.0
  - flask>=2.0.0
  - gunicorn>=20.0.0
  - RPi.GPIO>=0.7.0

---

## [1.0.0] - 2020-2025

### Initial Release
- Core functionality: GPIO relay control for garage door
- Three microservices: doorman, gate-api, button-sense
- Redis Streams for event-driven architecture
- Physical button support with short/long press detection
- Emergency brake feature
- Basic Flask API
- Systemd service files
- Mock GPIO for development

### Services
- **button_sense.py** - Physical button monitoring
- **gate_api.py** - REST API interface
- **doorman.py** - Door control logic

### Features
- Two-relay control (UP/DN)
- Door travel time management
- Emergency brake
- State tracking
- Event streaming
- Logging

---

## Version History Summary

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-03-16 | Complete overhaul: security, easy setup, monitoring |
| 1.0.0 | 2020-2025 | Initial working version |

---

## Upgrade Guide

### From 1.x to 2.0

1. **Backup your config:**
   ```bash
   cp gate_control/config.py config.py.backup
   ```

2. **Pull latest changes:**
   ```bash
   git pull
   ```

3. **Run setup script:**
   ```bash
   sudo ./setup.sh
   ```

4. **Update any API scripts:**
   - Add API key to all requests
   - Use header: `X-API-Key: your-key`

5. **Test:**
   ```bash
   ./gate.sh test
   ```

### Rollback

If issues occur:
```bash
# Restore old config
cp config.py.backup gate_control/config.py

# Restart services
./gate.sh restart
```

---

## Roadmap

### Near Future
- [ ] Add pytest tests
- [ ] Add web dashboard
- [ ] Add MQTT support for IoT integration
- [ ] Add Prometheus metrics endpoint

### Future Considerations
- [ ] Mobile app
- [ ] Multi-gate support
- [ ] Persistent database for event history
- [ ] Machine learning for door behavior
- [ ] Integration with smart home platforms

---

**Note:** This project follows semantic versioning. Major version changes may include breaking changes.
