#!/usr/bin/env python3
"""
Season Management Utility.

Interactive tool for managing sports seasons and viewing season information.
"""

import json
import sys
from datetime import date
from typing import Optional
from season_manager import SeasonManager, get_current_season, get_season_info, get_available_seasons


def display_season_info(sport: str, season_year: Optional[str] = None):
    """Display detailed information about a season."""
    if season_year is None:
        season_year = get_current_season(sport)
    
    try:
        season_info = get_season_info(sport, season_year)
        print(f"\n{sport.upper()} {season_year} Season Information:")
        print("=" * 50)
        print(f"Season Name: {season_info['name']}")
        print(f"Current Phase: {season_info['phase']}")
        if season_info['week']:
            print(f"Current Week: {season_info['week']}")
        print(f"API Base: {season_info['api_base']}")
        print("\nKey Dates:")
        dates = season_info['dates']
        print(f"  Pre-season start: {dates['pre_season_start']}")
        print(f"  Regular season start: {dates['regular_season_start']}")
        print(f"  Regular season end: {dates['regular_season_end']}")
        print(f"  Playoffs start: {dates['playoffs_start']}")
        print(f"  Playoffs end: {dates['playoffs_end']}")
        
    except Exception as e:
        print(f"Error getting season info: {e}")


def add_new_season():
    """Interactive function to add a new season."""
    print("\nAdd New Season")
    print("=" * 30)
    
    # Get sport
    sport = input("Enter sport (wnba/nba/nhl/mlb/nfl): ").lower().strip()
    if sport not in ['wnba', 'nba', 'nhl', 'mlb', 'nfl']:
        print("Invalid sport!")
        return
    
    # Get season year
    season_year = input("Enter season year (e.g., 2026): ").strip()
    if not season_year.isdigit():
        print("Invalid season year!")
        return
    
    # Get season name
    season_name = input(f"Enter season name (e.g., {sport.upper()} {season_year}): ").strip()
    if not season_name:
        season_name = f"{sport.upper()} {season_year}"
    
    # Get dates
    print("\nEnter season dates (YYYY-MM-DD format):")
    pre_season_start = input("Pre-season start date: ").strip()
    regular_season_start = input("Regular season start date: ").strip()
    regular_season_end = input("Regular season end date: ").strip()
    playoffs_start = input("Playoffs start date: ").strip()
    playoffs_end = input("Playoffs end date: ").strip()
    
    # Validate dates
    try:
        for date_str in [pre_season_start, regular_season_start, regular_season_end, playoffs_start, playoffs_end]:
            date.fromisoformat(date_str)
    except ValueError:
        print("Invalid date format! Use YYYY-MM-DD")
        return
    
    # Create season data
    season_data = {
        "name": season_name,
        "pre_season_start": pre_season_start,
        "regular_season_start": regular_season_start,
        "regular_season_end": regular_season_end,
        "playoffs_start": playoffs_start,
        "playoffs_end": playoffs_end,
        "api_base": f"https://api.sportsblaze.com/v1/{sport}"
    }
    
    # Add season
    try:
        season_manager = SeasonManager()
        season_manager.add_season(sport, season_year, season_data)
        print(f"\n✅ Successfully added {sport.upper()} {season_year} season!")
        display_season_info(sport, season_year)
    except Exception as e:
        print(f"Error adding season: {e}")


def list_all_seasons():
    """List all available seasons for all sports."""
    print("\nAll Available Seasons")
    print("=" * 30)
    
    sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
    
    for sport in sports:
        print(f"\n{sport.upper()}:")
        try:
            available_seasons = get_available_seasons(sport)
            current_season = get_current_season(sport)
            
            for season in sorted(available_seasons):
                marker = " (current)" if season == current_season else ""
                print(f"  {season}{marker}")
                
        except Exception as e:
            print(f"  Error: {e}")


def update_season():
    """Interactive function to update an existing season."""
    print("\nUpdate Season")
    print("=" * 30)
    
    # Get sport
    sport = input("Enter sport (wnba/nba/nhl/mlb/nfl): ").lower().strip()
    if sport not in ['wnba', 'nba', 'nhl', 'mlb', 'nfl']:
        print("Invalid sport!")
        return
    
    # Get available seasons
    try:
        available_seasons = get_available_seasons(sport)
        if not available_seasons:
            print(f"No seasons available for {sport}")
            return
        
        print(f"Available seasons for {sport}: {', '.join(available_seasons)}")
        season_year = input("Enter season year to update: ").strip()
        
        if season_year not in available_seasons:
            print("Season not found!")
            return
        
        # Get current season info
        season_manager = SeasonManager()
        current_data = season_manager.seasons_data["seasons"][sport][season_year]
        
        print(f"\nCurrent data for {sport} {season_year}:")
        for key, value in current_data.items():
            print(f"  {key}: {value}")
        
        # Get updates
        print("\nEnter new values (press Enter to keep current value):")
        season_name = input(f"Season name [{current_data['name']}]: ").strip()
        if season_name:
            current_data['name'] = season_name
        
        pre_season_start = input(f"Pre-season start [{current_data['pre_season_start']}]: ").strip()
        if pre_season_start:
            current_data['pre_season_start'] = pre_season_start
        
        regular_season_start = input(f"Regular season start [{current_data['regular_season_start']}]: ").strip()
        if regular_season_start:
            current_data['regular_season_start'] = regular_season_start
        
        regular_season_end = input(f"Regular season end [{current_data['regular_season_end']}]: ").strip()
        if regular_season_end:
            current_data['regular_season_end'] = regular_season_end
        
        playoffs_start = input(f"Playoffs start [{current_data['playoffs_start']}]: ").strip()
        if playoffs_start:
            current_data['playoffs_start'] = playoffs_start
        
        playoffs_end = input(f"Playoffs end [{current_data['playoffs_end']}]: ").strip()
        if playoffs_end:
            current_data['playoffs_end'] = playoffs_end
        
        # Update season
        season_manager.update_season(sport, season_year, current_data)
        print(f"\n✅ Successfully updated {sport.upper()} {season_year} season!")
        display_season_info(sport, season_year)
        
    except Exception as e:
        print(f"Error updating season: {e}")


def show_current_status():
    """Show current status of all sports."""
    print("\nCurrent Sports Status")
    print("=" * 30)
    
    sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
    
    for sport in sports:
        print(f"\n{sport.upper()}:")
        try:
            current_season = get_current_season(sport)
            season_info = get_season_info(sport, current_season)
            available_seasons = get_available_seasons(sport)
            
            print(f"  Current season: {current_season}")
            print(f"  Season name: {season_info['name']}")
            print(f"  Current phase: {season_info['phase']}")
            if season_info['week']:
                print(f"  Current week: {season_info['week']}")
            print(f"  Available seasons: {', '.join(available_seasons)}")
            
        except Exception as e:
            print(f"  Error: {e}")


def main():
    """Main interactive menu."""
    while True:
        print("\n" + "=" * 50)
        print("SEASON MANAGEMENT UTILITY")
        print("=" * 50)
        print("1. Show current status of all sports")
        print("2. List all available seasons")
        print("3. Display detailed season information")
        print("4. Add new season")
        print("5. Update existing season")
        print("6. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            show_current_status()
        elif choice == '2':
            list_all_seasons()
        elif choice == '3':
            sport = input("Enter sport (wnba/nba/nhl/mlb/nfl): ").lower().strip()
            if sport in ['wnba', 'nba', 'nhl', 'mlb', 'nfl']:
                season_year = input("Enter season year (or press Enter for current): ").strip()
                if not season_year:
                    season_year = None
                display_season_info(sport, season_year)
            else:
                print("Invalid sport!")
        elif choice == '4':
            add_new_season()
        elif choice == '5':
            update_season()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-6.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main() 