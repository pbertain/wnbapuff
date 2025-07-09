#!/usr/bin/env python3
"""
Test script for WNBA API endpoints.
"""

import requests
import json
import time

def test_flask_endpoints():
    """Test Flask curl-style endpoints."""
    base_url = "http://localhost:5001"
    
    print("Testing Flask endpoints...")
    
    # Test help endpoint
    try:
        response = requests.get(f"{base_url}/curl/help")
        print(f"✓ Help endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Help endpoint failed: {e}")
    
    # Test standings endpoint
    try:
        response = requests.get(f"{base_url}/curl/standings")
        print(f"✓ Standings endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Standings endpoint failed: {e}")
    
    # Test scores endpoint
    try:
        response = requests.get(f"{base_url}/curl/scores")
        print(f"✓ Scores endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Scores endpoint failed: {e}")
    
    # Test schedule endpoint
    try:
        response = requests.get(f"{base_url}/curl/schedule")
        print(f"✓ Schedule endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Schedule endpoint failed: {e}")

def test_fastapi_endpoints():
    """Test FastAPI JSON endpoints."""
    base_url = "http://localhost:8001"
    
    print("\nTesting FastAPI endpoints...")
    
    # Test scores endpoint
    try:
        response = requests.get(f"{base_url}/api/scores")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Scores endpoint: {response.status_code} ({len(data.get('games', []))} games)")
        else:
            print(f"✗ Scores endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Scores endpoint failed: {e}")
    
    # Test schedule endpoint
    try:
        response = requests.get(f"{base_url}/api/schedule")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Schedule endpoint: {response.status_code} ({len(data.get('games', []))} games)")
        else:
            print(f"✗ Schedule endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Schedule endpoint failed: {e}")
    
    # Test standings endpoint
    try:
        response = requests.get(f"{base_url}/api/standings")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Standings endpoint: {response.status_code}")
        else:
            print(f"✗ Standings endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Standings endpoint failed: {e}")

def test_optional_parameters():
    """Test endpoints with optional parameters."""
    print("\nTesting optional parameters...")
    
    # Test standings with league parameter
    try:
        response = requests.get("http://localhost:5001/curl/standings?group=league")
        print(f"✓ Standings with league parameter: {response.status_code}")
    except Exception as e:
        print(f"✗ Standings with league parameter failed: {e}")
    
    # Test scores with date parameter
    try:
        response = requests.get("http://localhost:5001/curl/scores?date=2025-07-08")
        print(f"✓ Scores with date parameter: {response.status_code}")
    except Exception as e:
        print(f"✗ Scores with date parameter failed: {e}")
    
    # Test JSON scores with date parameter
    try:
        response = requests.get("http://localhost:8001/api/scores?target_date=2025-07-08")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ JSON scores with date parameter: {response.status_code} ({len(data.get('games', []))} games)")
        else:
            print(f"✗ JSON scores with date parameter: {response.status_code}")
    except Exception as e:
        print(f"✗ JSON scores with date parameter failed: {e}")

def main():
    """Run all tests."""
    print("WNBA API Test Suite")
    print("=" * 50)
    
    # Wait a moment for servers to be ready
    print("Waiting for servers to be ready...")
    time.sleep(2)
    
    test_flask_endpoints()
    test_fastapi_endpoints()
    test_optional_parameters()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nAPI Documentation:")
    print("- Flask endpoints: http://localhost:5001/curl/help")
    print("- FastAPI docs: http://localhost:8001/docs")

if __name__ == "__main__":
    main() 