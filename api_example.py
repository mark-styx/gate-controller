#!/usr/bin/env python3
"""
Example: Using the Gate Controller API from Python

This script demonstrates how to interact with the gate controller API
programmatically. You can use this as a starting point for integrations.

Usage:
    python3 api_example.py
"""

import json
import requests
from pathlib import Path
import sys

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY_FILE = Path(__file__).parent / ".api_key"


def load_api_key():
    """Load API key from file or prompt user"""
    if API_KEY_FILE.exists():
        with open(API_KEY_FILE) as f:
            return f.read().strip().split("=")[1]
    
    # If not found, prompt user
    key = input("Enter your API key: ").strip()
    return key


class GateController:
    """Simple client for the Gate Controller API"""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
    
    def health_check(self):
        """Check API health (no auth required)"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_status(self):
        """Get current gate status"""
        response = requests.get(
            f"{self.base_url}/gate/status",
            headers=self.headers
        )
        return response.json()
    
    def activate(self):
        """Activate the gate"""
        response = requests.post(
            f"{self.base_url}/gate/activate",
            headers=self.headers
        )
        return response.json()
    
    def get_ebrake(self):
        """Get emergency brake status"""
        response = requests.get(
            f"{self.base_url}/gate/ebrake",
            headers=self.headers
        )
        return response.json()
    
    def toggle_ebrake(self):
        """Toggle emergency brake"""
        response = requests.post(
            f"{self.base_url}/gate/ebrake",
            headers=self.headers
        )
        return response.json()


def main():
    print("Gate Controller API Example")
    print("=" * 60)
    
    # Load API key
    try:
        api_key = load_api_key()
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(1)
    
    # Create client
    gate = GateController(API_BASE_URL, api_key)
    
    # Example 1: Health check
    print("\n1. Health Check (no auth required)")
    try:
        health = gate.health_check()
        print(json.dumps(health, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Example 2: Get gate status
    print("\n2. Get Gate Status")
    try:
        status = gate.get_status()
        print(json.dumps(status, indent=2))
        print(f"\nDoor is: {status.get('state')}")
        print(f"Ebrake: {'ACTIVE' if status.get('ebrake') == '1' else 'inactive'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Activate gate (commented out for safety)
    print("\n3. Activate Gate")
    print("(Commented out for safety - uncomment to test)")
    # try:
    #     confirm = input("Really activate the gate? (yes/no): ")
    #     if confirm.lower() == "yes":
    #         result = gate.activate()
    #         print(json.dumps(result, indent=2))
    #     else:
    #         print("Cancelled")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # Example 4: Check ebrake
    print("\n4. Emergency Brake Status")
    try:
        ebrake = gate.get_ebrake()
        print(json.dumps(ebrake, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Integration example
    print("\n5. Integration Example")
    print("Here's how you might use this in a real integration:")
    print("""
    # Wait for door to close
    import time
    
    # Activate gate
    gate.activate()
    print("Gate opening...")
    
    # Wait for it to open
    time.sleep(10)
    
    # Check status
    status = gate.get_status()
    if status['state'] == 'UP':
        print("Gate is open!")
        
        # Wait for car to enter
        time.sleep(15)
        
        # Gate should auto-close, or you can close it manually
        print("Waiting for gate to close...")
    """)
    
    print("\n" + "=" * 60)
    print("Examples complete!")


if __name__ == "__main__":
    main()
