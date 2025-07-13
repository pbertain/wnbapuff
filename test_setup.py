#!/usr/bin/env python3
"""
Test script to verify WNBA API setup and configuration.
"""

import sys
import os
from datetime import date

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✅ requests module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        import pytz
        print("✅ pytz module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pytz: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        from wnba_config import get_api_key, get_api_type
        print("✅ wnba_config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import wnba_config: {e}")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has API key."""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Create it with: touch .env")
        print("   Add your API key: SPORTSBLAZE_API_KEY=your_key_here")
        return False
    
    print("✅ .env file exists")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for API keys
    sportsblaze_key = os.getenv('SPORTSBLAZE_API_KEY')
    rapidapi_key = os.getenv('WNBA_API_KEY')
    
    if sportsblaze_key:
        print("✅ SPORTSBLAZE_API_KEY found")
        return True
    elif rapidapi_key:
        print("✅ WNBA_API_KEY found (legacy RapidAPI)")
        return True
    else:
        print("❌ No API key found in .env file")
        print("   Add one of these to your .env file:")
        print("   SPORTSBLAZE_API_KEY=your_key_here")
        print("   WNBA_API_KEY=your_key_here")
        return False

def test_api_config():
    """Test API configuration functions."""
    print("\nTesting API configuration...")
    
    try:
        from wnba_config import get_api_key, get_api_type
        
        api_type = get_api_type()
        print(f"✅ API type detected: {api_type}")
        
        api_key = get_api_key()
        if api_key:
            # Show first few characters of key for verification
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            print(f"✅ API key loaded: {masked_key}")
        else:
            print("❌ No API key available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API configuration: {e}")
        return False
    
    return True

def test_script_imports():
    """Test that main scripts can be imported."""
    print("\nTesting script imports...")
    
    scripts = ['wnba_scores', 'wnba_standings', 'wnba_schedule']
    
    for script in scripts:
        try:
            module = __import__(script)
            print(f"✅ {script}.py imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {script}.py: {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 WNBA API Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_env_file,
        test_api_config,
        test_script_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nYou can now run:")
        print("  python3 wnba_scores.py")
        print("  python3 wnba_standings.py")
        print("  python3 wnba_schedule.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 