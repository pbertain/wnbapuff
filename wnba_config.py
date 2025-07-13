#!/usr/bin/env python3
"""
WNBA Configuration Module.

Handles API key loading from environment variables for both RapidAPI and SportsBlaze.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key() -> str:
    """
    Get the WNBA API key from environment variables.
    
    Returns:
        The API key string
        
    Raises:
        ValueError: If no API key is found in environment variables
    """
    # Try SportsBlaze API key first (preferred)
    api_key = os.getenv('SPORTSBLAZE_API_KEY')
    if api_key:
        return api_key
    
    # Fallback to RapidAPI key for backward compatibility
    api_key = os.getenv('WNBA_API_KEY')
    if api_key:
        return api_key
    
    raise ValueError(
        "No API key found. Please set SPORTSBLAZE_API_KEY or WNBA_API_KEY "
        "in your .env file or environment variables."
    )

def get_api_type() -> str:
    """
    Determine which API type to use based on available environment variables.
    
    Returns:
        'sportsblaze' if SPORTSBLAZE_API_KEY is set, 'rapidapi' otherwise
    """
    if os.getenv('SPORTSBLAZE_API_KEY'):
        return 'sportsblaze'
    elif os.getenv('WNBA_API_KEY'):
        return 'rapidapi'
    else:
        raise ValueError("No API key found in environment variables") 