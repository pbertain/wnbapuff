#!/usr/bin/env python3
"""
Sports Configuration Module.

Handles API key loading and dynamic season management for multiple sports.
"""

import os
from dotenv import load_dotenv
from datetime import date, datetime
from typing import Dict, Any, Optional
from season_manager import get_season_info as get_dynamic_season_info, get_current_season as get_dynamic_current_season, get_available_seasons as get_dynamic_available_seasons

# Load environment variables from .env file
load_dotenv()

def get_api_key(sport: str = 'wnba') -> str:
    """
    Get the API key for a specific sport.
    
    Args:
        sport: The sport abbreviation (wnba, nba, nhl, mlb, nfl)
        
    Returns:
        The API key string
        
    Raises:
        ValueError: If no API key is found for the sport
    """
    # Try sport-specific API key first
    sport_key = os.getenv(f'{sport.upper()}_API_KEY')
    if sport_key:
        return sport_key
    
    # Fallback to general SportsBlaze key
    api_key = os.getenv('SPORTSBLAZE_API_KEY')
    if api_key:
        return api_key
    
    # Legacy RapidAPI support for WNBA
    if sport == 'wnba':
        api_key = os.getenv('WNBA_API_KEY')
        if api_key:
            return api_key
    
    raise ValueError(
        f"No API key found for {sport.upper()}. Please set {sport.upper()}_API_KEY "
        "or SPORTSBLAZE_API_KEY in your .env file or environment variables."
    )

def get_api_type(sport: str = 'wnba') -> str:
    """
    Determine which API type to use for a specific sport.
    
    Args:
        sport: The sport abbreviation
        
    Returns:
        'sportsblaze' if SportsBlaze API key is set, 'rapidapi' otherwise
    """
    if os.getenv('SPORTSBLAZE_API_KEY') or os.getenv(f'{sport.upper()}_API_KEY'):
        return 'sportsblaze'
    elif sport == 'wnba' and os.getenv('WNBA_API_KEY'):
        return 'rapidapi'
    else:
        raise ValueError(f"No API key found for {sport}")

def get_season_info(sport: str, target_date: Optional[date] = None, season_year: Optional[str] = None) -> Dict[str, Any]:
    """
    Get season information for a specific sport and date using dynamic season management.
    
    Args:
        sport: The sport abbreviation
        target_date: The date to check (defaults to today)
        season_year: The season year (if None, uses current season)
        
    Returns:
        Dictionary with season phase and week information
    """
    return get_dynamic_season_info(sport, season_year, target_date)

def get_current_season(sport: str, target_date: Optional[date] = None) -> str:
    """
    Get the current season year for a sport.
    
    Args:
        sport: The sport abbreviation
        target_date: The date to check (defaults to today)
        
    Returns:
        Season year as string (e.g., "2025")
    """
    return get_dynamic_current_season(sport, target_date)

def get_available_seasons(sport: str) -> list:
    """
    Get list of available seasons for a sport.
    
    Args:
        sport: The sport abbreviation
        
    Returns:
        List of available season years
    """
    return get_dynamic_available_seasons(sport)

def get_sport_info(sport: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a sport including current season status.
    
    Args:
        sport: The sport abbreviation
        
    Returns:
        Dictionary with sport information
    """
    try:
        current_season = get_current_season(sport)
        season_info = get_season_info(sport, season_year=current_season)
        available_seasons = get_available_seasons(sport)
        
        return {
            "sport": sport,
            "current_season": current_season,
            "season_info": season_info,
            "available_seasons": available_seasons,
            "api_type": get_api_type(sport),
            "has_api_key": bool(get_api_key(sport))
        }
    except Exception as e:
        return {
            "sport": sport,
            "error": str(e)
        }

def get_all_sports_info() -> Dict[str, Dict[str, Any]]:
    """
    Get information for all supported sports.
    
    Returns:
        Dictionary with information for all sports
    """
    sports = ["wnba", "nba", "nhl", "mlb", "nfl"]
    return {sport: get_sport_info(sport) for sport in sports}

def main():
    """Display current sports information."""
    print("Dynamic Sports Configuration")
    print("=" * 40)
    
    all_sports = get_all_sports_info()
    
    for sport, info in all_sports.items():
        print(f"\n{sport.upper()}:")
        if "error" in info:
            print(f"  Error: {info['error']}")
        else:
            print(f"  Current season: {info['current_season']}")
            print(f"  Season name: {info['season_info']['name']}")
            print(f"  Current phase: {info['season_info']['phase']}")
            if info['season_info']['week']:
                print(f"  Current week: {info['season_info']['week']}")
            print(f"  Available seasons: {', '.join(info['available_seasons'])}")
            print(f"  API type: {info['api_type']}")
            print(f"  Has API key: {info['has_api_key']}")


if __name__ == "__main__":
    main() 