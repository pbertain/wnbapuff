#!/usr/bin/env python3
"""
WNBA Standings Fetcher.

This script fetches and displays WNBA standings for the 2025 season.
It uses the wnba_dates module for accurate date calculations and season phase detection.
"""

import requests
import argparse
from datetime import datetime, date
import sys
import json
from typing import List, Dict, Any, Optional

# Import our custom date management module
from wnba_dates import WNBADates2025


def find_stat_by_name(stats: List[Dict[str, Any]], stat_name: str) -> Optional[Dict[str, Any]]:
    """
    Find a stat by its name in the stats array.
    
    Args:
        stats: Array of stat dictionaries
        stat_name: Name of the stat to find
        
    Returns:
        The stat dictionary if found, None otherwise
    """
    for stat in stats:
        if stat.get('name') == stat_name:
            return stat
    return None


def get_wnba_standings(json_data: Dict[str, Any], group: str, debug: bool = False) -> List[str]:
    """
    Process and return WNBA standings formatted by conference or league.

    Args:
        json_data: The API response containing standings data.
        group: Either 'conference' or 'league', indicating how to group the standings.
        debug: If True, print debug information about the data structure.

    Returns:
        A list of formatted strings representing the standings.
    """
    if debug:
        print("DEBUG: API Response Structure:")
        print(json.dumps(json_data, indent=2)[:2000] + "...")
        print("\nDEBUG: First conference structure:")
        if json_data.get('children') and len(json_data['children']) > 0:
            first_conf = json_data['children'][0]
            print(json.dumps(first_conf, indent=2)[:1000] + "...")
            if first_conf.get('standings', {}).get('entries') and len(first_conf['standings']['entries']) > 0:
                first_entry = first_conf['standings']['entries'][0]
                print("\nDEBUG: First team entry structure:")
                print(json.dumps(first_entry, indent=2)[:1000] + "...")
                if first_entry.get('stats'):
                    print("\nDEBUG: Stats array:")
                    for i, stat in enumerate(first_entry['stats']):
                        print(f"  [{i}] {stat}")

    standings = {"Eastern Conference": [], "Western Conference": []}

    for conference in json_data['children']:
        conference_name = conference['name']
        if conference_name in standings:
            standings[conference_name].extend(conference['standings']['entries'])
        else:
            print(f"Unexpected conference name: {conference_name}")

    def get_team_stats(entry):
        """Helper function to extract team stats safely."""
        wins_stat = find_stat_by_name(entry['stats'], 'wins')
        losses_stat = find_stat_by_name(entry['stats'], 'losses')
        games_behind_stat = find_stat_by_name(entry['stats'], 'gamesBehind')
        
        wins = int(wins_stat['value']) if wins_stat else 0
        losses = int(losses_stat['value']) if losses_stat else 0
        games_behind = float(games_behind_stat['value']) if games_behind_stat else 0.0
        
        return wins, losses, games_behind

    def sort_key(entry):
        """Helper function for sorting teams."""
        wins, losses, _ = get_team_stats(entry)
        return (wins, -losses)

    output_lines = []
    if group == "league":
        all_entries = standings["Eastern Conference"] + standings["Western Conference"]
        all_entries.sort(key=sort_key, reverse=True)
        
        for entry in all_entries:
            abbreviation = entry['team']['abbreviation']
            short_name = entry['team']['shortDisplayName']
            wins, losses, games_behind = get_team_stats(entry)
            
            team_info = f"{abbreviation} {short_name}".ljust(15)
            output_lines.append(f"{team_info} {wins:<2} - {losses:<2} GB: {games_behind:.1f}")
    else:
        for conference, entries in standings.items():
            output_lines.append(f"{conference}:")
            entries.sort(key=sort_key, reverse=True)
            
            for entry in entries:
                abbreviation = entry['team']['abbreviation']
                short_name = entry['team']['shortDisplayName']
                wins, losses, games_behind = get_team_stats(entry)
                
                team_info = f"{abbreviation} {short_name}".ljust(15)
                output_lines.append(f"{team_info} {wins:<2} - {losses:<2} GB: {games_behind:.1f}")
            output_lines.append("")  # Add a blank line between conferences

    if group == "conference" and output_lines[-1] == "":
        output_lines.pop()  # Remove the last blank line if exists

    return output_lines


def fetch_wnba_data() -> Optional[Dict[str, Any]]:
    """
    Fetch WNBA standings data from the API.

    Returns:
        JSON data from the API or None if there's an error.
    """
    from wnba_config import get_api_key
    
    url = "https://wnba-api.p.rapidapi.com/wnbastandings"
    querystring = {"year": "2025", "group": "conference"}
    headers = {
        "X-RapidAPI-Key": get_api_key(),
        "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching WNBA standings: {e}")
        return None


def main():
    """
    Main function to fetch WNBA standings and display them based on user input.
    """
    parser = argparse.ArgumentParser(description="Fetch WNBA standings for the 2025 season.")
    parser.add_argument(
        '--group', 
        type=str, 
        choices=['league', 'conference'], 
        default='conference', 
        help='Group type: league or conference'
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

    # Check if we're in the regular season
    current_phase, week_num = WNBADates2025.get_current_phase()
    
    if not WNBADates2025.is_regular_season():
        print(f"No results for WNBA Standings. Current phase: {current_phase}")
        print("This script only runs during the regular season.")
        return

    # Fetch data from API
    json_data = fetch_wnba_data()
    if not json_data:
        return

    # Process and display standings
    standings_lines = get_wnba_standings(json_data, args.group, args.debug)
    if not standings_lines:
        print("No standings data available.")
        return

    current_date_str = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M')

    print(f"\nWNBA standings for {current_date_str}:\n")
    for line in standings_lines:
        print(line)
    print(f"\nSeason: {current_phase} / wk: {week_num} - sent@{current_time_str}")


if __name__ == "__main__":
    main()

