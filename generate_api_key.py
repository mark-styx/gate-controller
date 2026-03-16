#!/usr/bin/env python3
"""
Generate a secure API key for the gate controller API.
Run this script and copy the output to your config.py file.
"""

import secrets
import sys

def generate_api_key():
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)

if __name__ == '__main__':
    key = generate_api_key()
    print("=" * 70)
    print("Generated API Key:")
    print("=" * 70)
    print(key)
    print("=" * 70)
    print("\nAdd this to your gate_control/config.py file:")
    print(f'API_KEY = \'{key}\'')
    print("\nTo use with curl:")
    print(f'curl -H "X-API-Key: {key}" http://localhost:8000/gate/status')
    print("\nOr with query parameter:")
    print(f'curl "http://localhost:8000/gate/status?api_key={key}"')
    print("=" * 70)
