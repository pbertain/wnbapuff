#!/usr/bin/env python3
"""
WNBA Scores Fetcher.

This script fetches and displays WNBA scores for today's games.
It uses the wnba_dates module for accurate date calculations and season phase detection.
"""

import requests
import argparse
from datetime import datetime, timedelta, date
import pytz
from typing import Dict, Any, Optional, List
import json

# Import our custom date management module
from wnba_dates import WNBADates2025


def fetch_wnba_scores(target_date: date) -> Optional[Dict[str, Any]]:
    """
    Fetch WNBA scores for a specific date.
    
    Args:
        target_date: The date to fetch scores for
        
    Returns:
        JSON data from the API or None if there's an error
    """
    from wnba_config import get_api_key
    
    url = "https://wnba-api.p.rapidapi.com/wnbascoreboard"
    querystring = {
        "year": target_date.strftime("%Y"),
        "month": target_date.strftime("%m"),
        "day": target_date.strftime("%d")
    }
    headers = {
        "X-RapidAPI-Key": get_api_key(),
        "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching WNBA scores: {e}")
        return None


def format_event(event: Dict[str, Any], local_timezone) -> str:
    """
    Format a single game event for display.
    
    Args:
        event: The game event data
        local_timezone: The local timezone for display
        
    Returns:
        Formatted string representing the game
    """
    try:
        competition = event['competitions'][0]
        competitors = competition['competitors']
        
        # Find home and away teams
        home_team = None
        away_team = None
        
        for competitor in competitors:
            if competitor.get('homeAway') == 'home':
                home_team = competitor
            elif competitor.get('homeAway') == 'away':
                away_team = competitor
        
        if not home_team or not away_team:
            return "Invalid game data"
        
        home_team_abbr = home_team['team']['abbreviation'].rjust(4)
        away_team_abbr = away_team['team']['abbreviation'].rjust(4)
        
        # Handle games that haven't started yet (no scores)
        home_score = home_team.get('score', '0')
        away_score = away_team.get('score', '0')
        
        # Get game status and period
        status = competition.get('status', {})
        status_type = status.get('type', {})
        status_name = status_type.get('name', 'Unknown')
        status_description = status_type.get('description', '')
        period = status.get('period', None)
        
        # Convert to integers if possible, otherwise show as scheduled
        try:
            home_score_int = int(home_score)
            away_score_int = int(away_score)
            
            if home_score_int >= away_score_int:
                game = f"{home_team_abbr} (h) [{home_score_int} - {away_score_int}] {away_team_abbr} (v)"
            else:
                game = f"{away_team_abbr} (v) [{away_score_int} - {home_score_int}] {home_team_abbr} (h)"
        except (ValueError, TypeError):
            # Game hasn't started yet
            game = f"{away_team_abbr} (v) [vs] {home_team_abbr} (h)"
        
        # Add status to the game line
        status_display = get_status_display(status_name, status_description, period)
        game += f" {status_display}"
        
        return game
        
    except (KeyError, IndexError) as e:
        return f"Error formatting game: {e}"


def get_status_display(status_name: str, status_description: str, period: Optional[int] = None) -> str:
    """
    Convert API status to a display-friendly format.
    
    Args:
        status_name: The status name from the API
        status_description: The status description from the API
        period: The current period number (if available)
        
    Returns:
        Formatted status string
    """
    # Handle overtime periods in progress first
    if period and period > 4:
        if status_name == 'STATUS_FINAL':
            # Final games with overtime
            if period == 5:
                return 'F/OT'
            elif period == 6:
                return 'F/2OT'
            elif period == 7:
                return 'F/3OT'
            elif period == 8:
                return 'F/4OT'
            else:
                return f'F/{period-4}OT'
        else:
            # Live overtime periods
            if period == 5:
                return 'OT'
            elif period == 6:
                return '2OT'
            elif period == 7:
                return '3OT'
            elif period == 8:
                return '4OT'
            else:
                return f'{period-4}OT'
    
    # Direct mapping for common statuses
    status_mapping = {
        'STATUS_SCHEDULED': 'Scheduled',
        'STATUS_IN_PROGRESS': 'Live',
        'STATUS_HALFTIME': 'H',
        'STATUS_FINAL': 'F',
        'STATUS_FINAL_OVERTIME': 'F/OT',
        'STATUS_POSTPONED': 'Postponed',
        'STATUS_CANCELLED': 'Cancelled',
        'STATUS_SUSPENDED': 'Suspended'
    }
    
    # Check if we have a direct mapping
    if status_name in status_mapping:
        return status_mapping[status_name]
    
    # Handle quarter-specific status from description
    if 'Q' in status_description:
        # Extract quarter number from description like "Q1", "Q2", etc.
        quarter_match = status_description.split()[-1]  # Get last word
        if quarter_match.startswith('Q'):
            return quarter_match
    
    # Handle halftime
    if 'HALF' in status_description.upper():
        return 'H'
    
    # Handle final
    if 'FINAL' in status_description.upper():
        return 'F'
    
    # Handle live games (in progress)
    if 'LIVE' in status_description.upper() or 'IN PROGRESS' in status_description.upper():
        return 'Live'
    
    # Default fallback - show the description if available, otherwise the name
    return status_description if status_description else status_name


def print_today_games(scores: Dict[str, Any], local_timezone, 
                      season_type: str, week_number: Optional[int], debug: bool = False) -> None:
    """
    Print today's WNBA games in a formatted way.
    
    Args:
        scores: The scores data from the API
        local_timezone: The local timezone for display
        season_type: The current season type
        week_number: The current week number (if applicable)
        debug: If True, print debug information about the API response
    """
    if debug:
        print("DEBUG: API Response Structure:")
        print(json.dumps(scores, indent=2)[:3000] + "...")
        if scores.get('events') and len(scores['events']) > 0:
            print("\nDEBUG: First event structure:")
            first_event = scores['events'][0]
            print(json.dumps(first_event, indent=2)[:1500] + "...")
            if first_event.get('competitions') and len(first_event['competitions']) > 0:
                first_competition = first_event['competitions'][0]
                print("\nDEBUG: First competition structure:")
                print(json.dumps(first_competition, indent=2)[:1000] + "...")
                if first_competition.get('status'):
                    print("\nDEBUG: Status structure:")
                    print(json.dumps(first_competition['status'], indent=2))

    events = scores.get('events', [])
    if not events:
        print("No games scheduled for the WNBA today.")
        return

    today_date = datetime.now(local_timezone).strftime("%a %d %b %y")
    print(f"WNBA scores for {today_date}:\n")

    for event in events:
        event_details = format_event(event, local_timezone)
        print(event_details)

    sent_time_str = datetime.now(local_timezone).strftime("%H:%M")
    
    if week_number:
        if season_type == "Regular Season":
            print(f"\nSeason: {season_type} / wk: {week_number} - sent@{sent_time_str}")
        elif season_type == "Playoffs":
            print(f"\nSeason: {season_type} / Playoff wk: {week_number} - sent@{sent_time_str}")
        else:
            print(f"\nSeason: {season_type} / wk: {week_number} - sent@{sent_time_str}")
    else:
        print(f"\nSeason: {season_type} - sent@{sent_time_str}")


def main():
    """
    Main function to fetch and display WNBA scores for today.
    """
    parser = argparse.ArgumentParser(description="Fetch WNBA scores for today's games.")
    parser.add_argument(
        '--date', 
        type=str, 
        help='Date to fetch scores for (YYYY-MM-DD format, defaults to today)'
    )
    parser.add_argument(
        '--timezone', 
        type=str, 
        default='America/Los_Angeles',
        help='Timezone for display (default: America/Los_Angeles)'
    )
    parser.add_argument(
        '--show-dates', 
        action='store_true', 
        help='Show the 2025 season schedule'
    )
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='Show debug information about API response structure'
    )
    args = parser.parse_args()

    # Show season dates if requested
    if args.show_dates:
        print("\n".join(WNBADates2025.get_season_summary()))
        return

    # Set up timezone
    try:
        local_timezone = pytz.timezone(args.timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Unknown timezone: {args.timezone}")
        print("Using America/Los_Angeles instead.")
        local_timezone = pytz.timezone("America/Los_Angeles")

    # Determine target date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            return
    else:
        # Use today's date
        target_date = date.today()

    # Check if we're in a valid season phase
    current_phase, week_num = WNBADates2025.get_current_phase(target_date)
    
    # Only show scores during regular season or playoffs
    if current_phase not in ["Regular Season", "Playoffs"]:
        print(f"No WNBA games during {current_phase}.")
        print("WNBA games are only played during Regular Season and Playoffs.")
        return

    # Fetch scores
    scores = fetch_wnba_scores(target_date)
    
    if not scores:
        print("Failed to fetch scores data.")
        return

    # Display the scores
    print_today_games(scores, local_timezone, current_phase, week_num, args.debug)


if __name__ == "__main__":
    main()