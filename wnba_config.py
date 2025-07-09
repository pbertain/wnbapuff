#!/usr/bin/env python3
"""
WNBA Configuration Module.

Handles API key loading from environment variables.
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
    api_key = os.getenv('WNBA_API_KEY')
    if not api_key:
        raise ValueError(
            "WNBA_API_KEY not found in environment variables. "
            "Please set WNBA_API_KEY in your .env file or environment."
        )
    return api_key 