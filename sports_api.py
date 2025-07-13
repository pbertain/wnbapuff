#!/usr/bin/env python3
"""
Generic Sports API Module.

Handles API calls for multiple sports with standardized endpoints and dynamic season management.
"""

import requests
from datetime import date
from typing import Dict, Any, Optional
from sports_config import get_api_key, get_api_type, get_season_info

def fetch_sports_standings(sport: str, group: str = "conference", season_year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch standings data for any sport.
    
    Args:
        sport: The sport abbreviation (wnba, nba, nhl, mlb, nfl)
        group: Either 'conference' or 'league'
        season_year: The season year (if None, uses current season)
        
    Returns:
        JSON data from the API or None if there's an error
    """
    try:
        api_type = get_api_type(sport)
        api_key = get_api_key(sport)
        season_info = get_season_info(sport, season_year=season_year)
        
        if api_type == 'sportsblaze':
            url = f"{season_info['api_base']}/standings"
            querystring = {"season": season_info['season_year']}
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        else:  # rapidapi (legacy for WNBA)
            url = "https://wnba-api.p.rapidapi.com/wnbastandings"
            querystring = {"year": season_info['season_year'], "group": group}
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
            }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"Error fetching {sport.upper()} standings: {e}")
        return None

def fetch_sports_scores(sport: str, target_date: date, season_year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch scores data for any sport.
    
    Args:
        sport: The sport abbreviation
        target_date: The date to fetch scores for
        season_year: The season year (if None, uses current season)
        
    Returns:
        JSON data from the API or None if there's an error
    """
    try:
        api_type = get_api_type(sport)
        api_key = get_api_key(sport)
        season_info = get_season_info(sport, target_date, season_year)
        
        if api_type == 'sportsblaze':
            url = f"{season_info['api_base']}/scores"
            querystring = {
                "date": target_date.strftime("%Y-%m-%d"),
                "season": season_info['season_year']
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        else:  # rapidapi (legacy for WNBA)
            url = "https://wnba-api.p.rapidapi.com/wnbascoreboard"
            querystring = {
                "year": target_date.strftime("%Y"),
                "month": target_date.strftime("%m"),
                "day": target_date.strftime("%d")
            }
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
            }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"Error fetching {sport.upper()} scores: {e}")
        return None

def fetch_sports_schedule(sport: str, target_date: date, season_year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch schedule data for any sport.
    
    Args:
        sport: The sport abbreviation
        target_date: The date to fetch schedule for
        season_year: The season year (if None, uses current season)
        
    Returns:
        JSON data from the API or None if there's an error
    """
    try:
        api_type = get_api_type(sport)
        api_key = get_api_key(sport)
        season_info = get_season_info(sport, target_date, season_year)
        
        if api_type == 'sportsblaze':
            url = f"{season_info['api_base']}/schedule"
            querystring = {
                "date": target_date.strftime("%Y-%m-%d"),
                "season": season_info['season_year']
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        else:  # rapidapi (legacy for WNBA)
            url = "https://wnba-api.p.rapidapi.com/wnbascoreboard"
            querystring = {
                "year": target_date.strftime("%Y"),
                "month": target_date.strftime("%m"),
                "day": target_date.strftime("%d")
            }
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
            }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"Error fetching {sport.upper()} schedule: {e}")
        return None

def format_sports_standings(json_data: Dict[str, Any], sport: str, group: str = "conference", season_year: Optional[str] = None) -> str:
    """
    Format standings data for display.
    
    Args:
        json_data: The API response data
        sport: The sport abbreviation
        group: Either 'conference' or 'league'
        season_year: The season year (if None, uses current season)
        
    Returns:
        Formatted standings string
    """
    if not json_data or 'children' not in json_data:
        return f"No {sport.upper()} standings data available."
    
    season_info = get_season_info(sport, season_year=season_year)
    output_lines = []
    output_lines.append(f"{sport.upper()} standings for {date.today().strftime('%Y-%m-%d')}:")
    output_lines.append(f"Season: {season_info['name']}")
    output_lines.append("")
    
    if group == "league":
        # Combine all teams into one list
        all_teams = []
        for conference in json_data.get('children', []):
            entries = conference.get('standings', {}).get('entries', [])
            all_teams.extend(entries)
        
        # Sort by wins (simplified)
        all_teams.sort(key=lambda x: int(next((stat['value'] for stat in x.get('stats', []) if stat.get('name') == 'wins'), 0)), reverse=True)
        
        for entry in all_teams:
            team_info = entry['team']
            abbreviation = team_info['abbreviation']
            short_name = team_info['shortDisplayName']
            
            # Find wins and losses
            wins = next((int(stat['value']) for stat in entry.get('stats', []) if stat.get('name') == 'wins'), 0)
            losses = next((int(stat['value']) for stat in entry.get('stats', []) if stat.get('name') == 'losses'), 0)
            
            team_info = f"{abbreviation} {short_name}".ljust(15)
            output_lines.append(f"{team_info} {wins:<2} - {losses:<2}")
    else:
        # Show by conference
        for conference in json_data.get('children', []):
            conference_name = conference['name']
            output_lines.append(f"{conference_name}:")
            
            entries = conference.get('standings', {}).get('entries', [])
            for entry in entries:
                team_info = entry['team']
                abbreviation = team_info['abbreviation']
                short_name = team_info['shortDisplayName']
                
                # Find wins and losses
                wins = next((int(stat['value']) for stat in entry.get('stats', []) if stat.get('name') == 'wins'), 0)
                losses = next((int(stat['value']) for stat in entry.get('stats', []) if stat.get('name') == 'losses'), 0)
                
                team_info = f"{abbreviation} {short_name}".ljust(15)
                output_lines.append(f"{team_info} {wins:<2} - {losses:<2}")
            output_lines.append("")
    
    # Remove trailing empty line
    if output_lines and output_lines[-1] == "":
        output_lines.pop()
    
    output_lines.append(f"Season: {season_info['phase']}")
    if season_info['week']:
        output_lines.append(f"Week: {season_info['week']}")
    
    return "\n".join(output_lines) 