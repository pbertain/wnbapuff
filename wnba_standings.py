#!/usr/bin/env python3

import requests
import argparse
from datetime import datetime
import sys

# Function to determine the current week number
def determine_week(start_date_str, current_date_str):
    """
    Calculate the week number in the WNBA season.

    Args:
        start_date_str (str): The season's start date as a string (YYYY-MM-DD).
        current_date_str (str): The current date as a string (YYYY-MM-DD).

    Returns:
        int: The current week number in the season.
    """
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
    return ((current_date - start_date).days // 7) + 1

# Function to process and format the standings
def get_wnba_standings(json_data, group):
    """
    Process and return WNBA standings formatted by conference or league.

    Args:
        json_data (dict): The API response containing standings data.
        group (str): Either 'conference' or 'league', indicating how to group the standings.

    Returns:
        list: A list of formatted strings representing the standings.
    """
    standings = {"Eastern Conference": [], "Western Conference": []}

    for conference in json_data['children']:
        conference_name = conference['name']
        if conference_name in standings:
            standings[conference_name].extend(conference['standings']['entries'])
        else:
            print(f"Unexpected conference name: {conference_name}")

    output_lines = []
    if group == "league":
        all_entries = standings["Eastern Conference"] + standings["Western Conference"]
        all_entries.sort(key=lambda x: (int(x['stats'][11]['value']), -int(x['stats'][6]['value'])), reverse=True)
        for entry in all_entries:
            abbreviation = entry['team']['abbreviation']
            short_name = entry['team']['shortDisplayName']
            wins = int(entry['stats'][11]['value'])
            losses = int(entry['stats'][6]['value'])
            games_behind = float(entry['stats'][4]['value'])  # Using the 'gamesbehind' key
            team_info = f"{abbreviation} {short_name}".ljust(15)
            output_lines.append(f"{team_info} {wins:<2} - {losses:<2} GB: {games_behind:.1f}")
    else:
        for conference, entries in standings.items():
            output_lines.append(f"{conference}:")
            entries.sort(key=lambda x: (int(x['stats'][11]['value']), -int(x['stats'][6]['value'])), reverse=True)
            for entry in entries:
                abbreviation = entry['team']['abbreviation']
                short_name = entry['team']['shortDisplayName']
                wins = int(entry['stats'][11]['value'])
                losses = int(entry['stats'][6]['value'])
                games_behind = float(entry['stats'][4]['value'])  # Using the 'gamesbehind' key
                team_info = f"{abbreviation} {short_name}".ljust(15)
                output_lines.append(f"{team_info} {wins:<2} - {losses:<2} GB: {games_behind:.1f}")
            output_lines.append("")  # Add a blank line between conferences

    if group == "conference" and output_lines[-1] == "":
        output_lines.pop()  # Remove the last blank line if exists

    return output_lines

# Function to get the current season type
def get_current_season_type(seasons, current_date_str):
    """
    Determines the current WNBA season type.

    Args:
        seasons (list): A list of seasons with start and end dates.
        current_date_str (str): The current date as a string (YYYY-MM-DD).

    Returns:
        tuple: The season type (str) and season year (str or None).
    """
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d')

    for season in seasons:
        for season_type in season['types']:
            start_date = datetime.strptime(season_type['startDate'][:10], '%Y-%m-%d')
            end_date = datetime.strptime(season_type['endDate'][:10], '%Y-%m-%d')
            if start_date <= current_date <= end_date:
                return season_type['name'], season['year']

    return "Off Season", None

# Main function to fetch data and display standings
def main():
    """
    Main function to fetch WNBA standings and display them based on user input.
    """
    parser = argparse.ArgumentParser(description="Fetch WNBA standings.")
    parser.add_argument('--group', type=str, choices=['league', 'conference'], default='conference', help='Group type: league or conference')
    args = parser.parse_args()

    url = "https://wnba-api.p.rapidapi.com/wnbastandings"
    querystring = {"year": "2024", "group": "conference"}  # Always fetch by conference
    headers = {
        "X-RapidAPI-Key": "a1dff23520mshe54eca80fd7e266p171832jsn90f79381d0b9",
        "X-RapidAPI-Host": "wnba-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an exception for bad HTTP status codes
    except requests.RequestException as e:
        print(f"Error fetching WNBA standings: {e}")
        return

    json_data = response.json()

    current_date_str = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M')

    current_season_type, current_season_year = get_current_season_type(json_data['seasons'], current_date_str)

    if current_season_type != "Regular Season":
        print("No results for WNBA Standings. This only runs during the regular season. Exiting now.")
        return

    standings_lines = get_wnba_standings(json_data, args.group)
    if not standings_lines:
        return

    week_number = determine_week("2024-05-14", current_date_str)

    print(f"\nWNBA standings for {current_date_str}:\n")
    for line in standings_lines:
        print(line)
    print(f"\nSeason: {current_season_type} / wk: {week_number} - sent@{current_time_str}")

# Call main function
if __name__ == "__main__":
    main()

