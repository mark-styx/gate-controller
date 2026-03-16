#!/usr/bin/env python3
"""
Gate Controller Monitoring Script

Simple monitoring that checks system health and sends alerts.
Can be run as a cron job or standalone.

Usage:
    python3 monitor.py [--alert-script /path/to/alert.sh]
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
import redis

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from gate_control import REVERE, MOCK
from gate_control.config import DOOR_TRAVEL_TIME

class GateMonitor:
    def __init__(self, alert_script=None):
        self.alert_script = alert_script
        self.issues = []
        self.checks_performed = 0
        self.checks_passed = 0
        
    def alert(self, message, level='WARNING'):
        """Send alert via configured method"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_msg = f"[{timestamp}] [{level}] {message}"
        
        print(alert_msg)
        
        if self.alert_script:
            import subprocess
            try:
                subprocess.run([self.alert_script, level, message], check=True)
            except Exception as e:
                print(f"Failed to send alert: {e}")
    
    def check_redis(self):
        """Check Redis connection"""
        self.checks_performed += 1
        try:
            REVERE.ping()
            self.checks_passed += 1
            return True
        except Exception as e:
            self.issues.append(f"Redis connection failed: {e}")
            self.alert("Redis connection failed!", 'CRITICAL')
            return False
    
    def check_api(self):
        """Check API health endpoint"""
        self.checks_performed += 1
        try:
            import urllib.request
            with urllib.request.urlopen('http://localhost:8000/health', timeout=5) as response:
                data = json.loads(response.read())
                if data.get('status') == 'healthy':
                    self.checks_passed += 1
                    return True
                else:
                    self.issues.append(f"API unhealthy: {data}")
                    self.alert("API is unhealthy", 'WARNING')
                    return False
        except Exception as e:
            self.issues.append(f"API check failed: {e}")
            self.alert("API not responding!", 'CRITICAL')
            return False
    
    def check_services(self):
        """Check systemd services are running"""
        import subprocess
        
        services = ['doorman', 'gate-api', 'button-sense']
        
        for service in services:
            self.checks_performed += 1
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', f'{service}.service'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    self.checks_passed += 1
                else:
                    self.issues.append(f"Service {service} is not running")
                    self.alert(f"Service {service} stopped!", 'CRITICAL')
            except Exception as e:
                self.issues.append(f"Failed to check service {service}: {e}")
    
    def check_door_state(self):
        """Check door state is reasonable"""
        self.checks_performed += 1
        try:
            state = REVERE.get('state')
            if state in ['DN', 'UP', 'Opening', 'Closing']:
                self.checks_passed += 1
                return True
            else:
                self.issues.append(f"Invalid door state: {state}")
                self.alert(f"Door in invalid state: {state}", 'WARNING')
                return False
        except Exception as e:
            self.issues.append(f"Failed to check door state: {e}")
    
    def check_door_timeout(self):
        """Check if door has been moving too long"""
        try:
            state = REVERE.get('state')
            if state in ['Opening', 'Closing']:
                t = float(REVERE.get('t') or 0)
                elapsed = time.time() - t
                
                if elapsed > DOOR_TRAVEL_TIME * 2:
                    self.issues.append(f"Door {state} for {elapsed:.1f}s (expected {DOOR_TRAVEL_TIME}s)")
                    self.alert(f"Door stuck {state} for {elapsed:.1f}s!", 'CRITICAL')
        except Exception as e:
            self.issues.append(f"Failed to check door timeout: {e}")
    
    def check_ebrake(self):
        """Check emergency brake status"""
        try:
            ebrake = REVERE.get('ebrake')
            if ebrake == '1':
                self.alert("Emergency brake is ACTIVE", 'INFO')
        except Exception as e:
            self.issues.append(f"Failed to check ebrake: {e}")
    
    def check_log_size(self):
        """Check if logs are getting large"""
        self.checks_performed += 1
        try:
            log_dir = Path.home() / 'logs'
            if log_dir.exists():
                total_size = sum(f.stat().st_size for f in log_dir.glob('*.txt'))
                size_mb = total_size / (1024 * 1024)
                
                if size_mb > 100:  # More than 100MB
                    self.alert(f"Logs are large: {size_mb:.1f}MB", 'WARNING')
                else:
                    self.checks_passed += 1
        except Exception as e:
            self.issues.append(f"Failed to check log size: {e}")
    
    def run_checks(self):
        """Run all monitoring checks"""
        print(f"Gate Controller Monitor - {datetime.now()}")
        print("=" * 60)
        
        self.check_redis()
        self.check_api()
        self.check_services()
        self.check_door_state()
        self.check_door_timeout()
        self.check_ebrake()
        self.check_log_size()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"Checks: {self.checks_passed}/{self.checks_performed} passed")
        
        if self.issues:
            print(f"\nIssues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")
            return False
        else:
            print("\n✓ All checks passed")
            return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Gate Controller Monitor')
    parser.add_argument('--alert-script', help='Script to call for alerts')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    monitor = GateMonitor(alert_script=args.alert_script)
    healthy = monitor.run_checks()
    
    if args.json:
        print(json.dumps({
            'healthy': healthy,
            'checks_performed': monitor.checks_performed,
            'checks_passed': monitor.checks_passed,
            'issues': monitor.issues,
            'timestamp': datetime.now().isoformat()
        }, indent=2))
    
    sys.exit(0 if healthy else 1)

if __name__ == '__main__':
    main()
