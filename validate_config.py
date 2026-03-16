#!/usr/bin/env python3
"""
Validate the gate controller configuration before running.
Checks for common issues and misconfigurations.
"""

import sys
from pathlib import Path

def check_api_key():
    """Check if API key has been changed from default"""
    try:
        from gate_control.config import API_KEY
        
        if API_KEY == 'your-secret-api-key-here-change-this':
            print("❌ ERROR: API_KEY is still set to default value!")
            print("   Run: python3 generate_api_key.py")
            print("   Then update gate_control/config.py with the generated key")
            return False
        
        if len(API_KEY) < 32:
            print("⚠️  WARNING: API_KEY is short (< 32 chars). Consider generating a longer key.")
            return True
        
        print("✓ API_KEY is configured")
        return True
    except ImportError as e:
        print(f"❌ ERROR: Cannot import config: {e}")
        return False

def check_redis_connection():
    """Check if Redis is accessible"""
    try:
        import redis
        client = redis.Redis(decode_responses=True)
        client.ping()
        print("✓ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ ERROR: Cannot connect to Redis: {e}")
        print("   Ensure Redis is running: sudo systemctl start redis-server")
        return False

def check_gpio():
    """Check GPIO availability"""
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        print("✓ GPIO available (running on Raspberry Pi)")
        return True
    except ImportError:
        print("⚠️  WARNING: RPi.GPIO not available (development mode)")
        print("   Using MockGPIO - relays won't actually trigger")
        return True
    except Exception as e:
        print(f"⚠️  WARNING: GPIO check failed: {e}")
        return True

def check_config_values():
    """Validate configuration values"""
    try:
        from gate_control.config import (
            DOOR_TRAVEL_TIME, CADENCE, PULSE, 
            SWITCH_EBRAKE, SWITCH_THRESHOLD, LOG_LEVEL
        )
        
        issues = []
        
        if DOOR_TRAVEL_TIME <= 0:
            issues.append("DOOR_TRAVEL_TIME must be positive")
        
        if CADENCE <= 0 or CADENCE > 1:
            issues.append("CADENCE should be between 0 and 1 second")
        
        if PULSE <= 0 or PULSE > 5:
            issues.append("PULSE should be between 0 and 5 seconds")
        
        if SWITCH_EBRAKE <= 0:
            issues.append("SWITCH_EBRAKE must be positive")
        
        if SWITCH_THRESHOLD <= 0 or SWITCH_THRESHOLD >= SWITCH_EBRAKE:
            issues.append("SWITCH_THRESHOLD should be between 0 and SWITCH_EBRAKE")
        
        if LOG_LEVEL < 0:
            issues.append("LOG_LEVEL should be 0 or greater")
        
        if issues:
            print("⚠️  WARNING: Configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return True
        
        print("✓ Configuration values look reasonable")
        return True
    except ImportError as e:
        print(f"❌ ERROR: Cannot import config: {e}")
        return False

def check_log_directory():
    """Check if log directory exists or can be created"""
    try:
        log_dir = Path.home() / 'logs'
        if not log_dir.exists():
            print(f"⚠️  Log directory doesn't exist: {log_dir}")
            print("   It will be created automatically")
        else:
            print(f"✓ Log directory exists: {log_dir}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Cannot check log directory: {e}")
        return False

def main():
    print("=" * 70)
    print("Gate Controller Configuration Validation")
    print("=" * 70)
    print()
    
    checks = [
        ("API Key", check_api_key),
        ("Redis Connection", check_redis_connection),
        ("GPIO Availability", check_gpio),
        ("Configuration Values", check_config_values),
        ("Log Directory", check_log_directory),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        print("-" * 70)
        results.append(check_func())
        print()
    
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✓ All checks passed ({passed}/{total})")
        print("\nYou're ready to run the gate controller!")
        print("\nStart services:")
        print("  sudo systemctl start doorman")
        print("  sudo systemctl start gate-api")
        print("  sudo systemctl start button-sense")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\nPlease fix the issues above before running the gate controller.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
