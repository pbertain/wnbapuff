#!/usr/bin/env python3
"""
WNBA Schedule Fetcher.

Fetches and displays the WNBA schedule for a given date, using modular season logic from wnba_dates.py.
"""

import requests
import argparse
from datetime import datetime, date
import pytz
from typing import Dict, Any, Optional
import json

from wnba_dates import WNBADates2025


def fetch_wnba_schedule(target_date: date) -> Optional[Dict[str, Any]]:
    """
    Fetch WNBA schedule for a specific date.
    Args:
        target_date: The date to fetch schedule for
    Returns:
        JSON data from the API or None if there's an error
    """
    from wnba_config import get_api_key, get_api_type
    
    api_type = get_api_type()
    
    if api_type == 'sportsblaze':
        url = "https://api.sportsblaze.com/v1/wnba/schedule"
        querystring = {
            "date": target_date.strftime("%Y-%m-%d")
        }
        headers = {
            "Authorization": f"Bearer {get_api_key()}",
            "Content-Type": "application/json"
        }
    else:  # rapidapi
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
        print(f"Error fetching WNBA schedule: {e}")
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
        # Show records if available
        home_record = home_team.get('records', [{}])[0].get('summary', '')
        away_record = away_team.get('records', [{}])[0].get('summary', '')
        if home_record and away_record:
            home_wins, home_losses = home_record.split('-')
            away_wins, away_losses = away_record.split('-')
            game = (f"{away_team_abbr} (v) [{away_wins.strip():2} - {away_losses.strip():2}] "
                    f"- {home_team_abbr} [{home_wins.strip():2} - {home_losses.strip():2}] (h)")
        else:
            game = f"{away_team_abbr} (v) - {home_team_abbr} (h)"
        return game
    except Exception as e:
        return f"Error formatting game: {e}"


def print_schedule(schedule: Dict[str, Any], local_timezone, season_type: str, week_number: Optional[int], debug: bool = False) -> None:
    """
    Print the WNBA schedule for the given date.
    Args:
        schedule: The schedule data from the API
        local_timezone: The local timezone for display
        season_type: The current season type
        week_number: The current week number (if applicable)
        debug: If True, print debug information about the API response
    """
    if debug:
        print("DEBUG: API Response Structure:")
        print(json.dumps(schedule, indent=2)[:3000] + "...")
        if schedule.get('events') and len(schedule['events']) > 0:
            print("\nDEBUG: First event structure:")
            first_event = schedule['events'][0]
            print(json.dumps(first_event, indent=2)[:1500] + "...")
    events = schedule.get('events', [])
    if not events:
        print("No games scheduled for the WNBA today.")
        return
    today_date = datetime.now(local_timezone).strftime("%a %d %b %y")
    print(f"WNBA schedule for {today_date}:\n")
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
    Main function to fetch and display WNBA schedule for a given date.
    """
    parser = argparse.ArgumentParser(description="Fetch WNBA schedule for a given date.")
    parser.add_argument(
        '--date',
        type=str,
        help='Date to fetch schedule for (YYYY-MM-DD format, defaults to today)'
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

    if args.show_dates:
        print("\n".join(WNBADates2025.get_season_summary()))
        return
    try:
        local_timezone = pytz.timezone(args.timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Unknown timezone: {args.timezone}")
        print("Using America/Los_Angeles instead.")
        local_timezone = pytz.timezone("America/Los_Angeles")
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            return
    else:
        target_date = date.today()
    # Use WNBADates2025 for season phase and week
    season_type, week_number = WNBADates2025.get_current_phase(target_date)
    schedule = fetch_wnba_schedule(target_date)
    if not schedule:
        print("Failed to fetch schedule data.")
        return
    print_schedule(schedule, local_timezone, season_type, week_number, args.debug)


if __name__ == "__main__":
    main()
