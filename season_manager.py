#!/usr/bin/env python3
"""
Dynamic Season Management Module.

Handles automatic season detection, transitions, and multi-season support.
"""

import json
import os
from datetime import date, datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path


class SeasonManager:
    """Dynamic season management for multiple sports."""
    
    def __init__(self, seasons_file: str = "seasons.json"):
        """
        Initialize the season manager.
        
        Args:
            seasons_file: Path to the JSON file containing season data
        """
        self.seasons_file = seasons_file
        self.seasons_data = self._load_seasons_data()
    
    def _load_seasons_data(self) -> Dict[str, Any]:
        """Load season data from JSON file or create default if not exists."""
        try:
            if os.path.exists(self.seasons_file):
                with open(self.seasons_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default seasons data
                default_data = self._create_default_seasons()
                self._save_seasons_data(default_data)
                return default_data
        except Exception as e:
            print(f"Warning: Could not load seasons data: {e}")
            return self._create_default_seasons()
    
    def _save_seasons_data(self, data: Dict[str, Any]) -> None:
        """Save season data to JSON file."""
        try:
            with open(self.seasons_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save seasons data: {e}")
    
    def _create_default_seasons(self) -> Dict[str, Any]:
        """Create default season data structure."""
        current_year = date.today().year
        
        return {
            "seasons": {
                "wnba": {
                    "2025": {
                        "name": "WNBA 2025",
                        "pre_season_start": "2025-05-02",
                        "regular_season_start": "2025-05-16",
                        "regular_season_end": "2025-09-11",
                        "playoffs_start": "2025-09-14",
                        "playoffs_end": "2025-10-19",
                        "api_base": "https://api.sportsblaze.com/v1/wnba"
                    },
                    "2026": {
                        "name": "WNBA 2026",
                        "pre_season_start": "2026-05-02",
                        "regular_season_start": "2026-05-16",
                        "regular_season_end": "2026-09-11",
                        "playoffs_start": "2026-09-14",
                        "playoffs_end": "2026-10-19",
                        "api_base": "https://api.sportsblaze.com/v1/wnba"
                    }
                },
                "nba": {
                    "2025": {
                        "name": "NBA 2025-26",
                        "pre_season_start": "2025-10-01",
                        "regular_season_start": "2025-10-21",
                        "regular_season_end": "2026-04-13",
                        "playoffs_start": "2026-04-19",
                        "playoffs_end": "2026-06-23",
                        "api_base": "https://api.sportsblaze.com/v1/nba"
                    },
                    "2026": {
                        "name": "NBA 2026-27",
                        "pre_season_start": "2026-10-01",
                        "regular_season_start": "2026-10-21",
                        "regular_season_end": "2027-04-13",
                        "playoffs_start": "2027-04-19",
                        "playoffs_end": "2027-06-23",
                        "api_base": "https://api.sportsblaze.com/v1/nba"
                    }
                },
                "nhl": {
                    "2025": {
                        "name": "NHL 2025-26",
                        "pre_season_start": "2025-09-15",
                        "regular_season_start": "2025-10-07",
                        "regular_season_end": "2026-04-19",
                        "playoffs_start": "2026-04-23",
                        "playoffs_end": "2026-06-15",
                        "api_base": "https://api.sportsblaze.com/v1/nhl"
                    },
                    "2026": {
                        "name": "NHL 2026-27",
                        "pre_season_start": "2026-09-15",
                        "regular_season_start": "2026-10-07",
                        "regular_season_end": "2027-04-19",
                        "playoffs_start": "2027-04-23",
                        "playoffs_end": "2027-06-15",
                        "api_base": "https://api.sportsblaze.com/v1/nhl"
                    }
                },
                "mlb": {
                    "2025": {
                        "name": "MLB 2025",
                        "pre_season_start": "2025-02-15",
                        "regular_season_start": "2025-03-27",
                        "regular_season_end": "2025-09-28",
                        "playoffs_start": "2025-10-01",
                        "playoffs_end": "2025-11-05",
                        "api_base": "https://api.sportsblaze.com/v1/mlb"
                    },
                    "2026": {
                        "name": "MLB 2026",
                        "pre_season_start": "2026-02-15",
                        "regular_season_start": "2026-03-27",
                        "regular_season_end": "2026-09-28",
                        "playoffs_start": "2026-10-01",
                        "playoffs_end": "2026-11-05",
                        "api_base": "https://api.sportsblaze.com/v1/mlb"
                    }
                },
                "nfl": {
                    "2025": {
                        "name": "NFL 2025-26",
                        "pre_season_start": "2025-08-07",
                        "regular_season_start": "2025-09-04",
                        "regular_season_end": "2026-01-05",
                        "playoffs_start": "2026-01-11",
                        "playoffs_end": "2026-02-08",
                        "api_base": "https://api.sportsblaze.com/v1/nfl"
                    },
                    "2026": {
                        "name": "NFL 2026-27",
                        "pre_season_start": "2026-08-07",
                        "regular_season_start": "2026-09-04",
                        "regular_season_end": "2027-01-05",
                        "playoffs_start": "2027-01-11",
                        "playoffs_end": "2027-02-08",
                        "api_base": "https://api.sportsblaze.com/v1/nfl"
                    }
                }
            },
            "settings": {
                "auto_detect_season": True,
                "default_season": "current",
                "supported_sports": ["wnba", "nba", "nhl", "mlb", "nfl"]
            }
        }
    
    def get_current_season(self, sport: str, target_date: Optional[date] = None) -> str:
        """
        Get the current season year for a sport.
        
        Args:
            sport: The sport abbreviation
            target_date: The date to check (defaults to today)
            
        Returns:
            Season year as string (e.g., "2025")
        """
        if target_date is None:
            target_date = date.today()
        
        if sport not in self.seasons_data["seasons"]:
            raise ValueError(f"Unknown sport: {sport}")
        
        # Find the season that contains the target date
        for season_year, season_data in self.seasons_data["seasons"][sport].items():
            season_start = datetime.strptime(season_data["pre_season_start"], "%Y-%m-%d").date()
            season_end = datetime.strptime(season_data["playoffs_end"], "%Y-%m-%d").date()
            
            if season_start <= target_date <= season_end:
                return season_year
        
        # If no season found, return the most recent season
        available_seasons = list(self.seasons_data["seasons"][sport].keys())
        if available_seasons:
            return max(available_seasons)
        
        # Fallback to current year
        return str(target_date.year)
    
    def get_season_info(self, sport: str, season_year: Optional[str] = None, 
                       target_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Get season information for a sport and season.
        
        Args:
            sport: The sport abbreviation
            season_year: The season year (if None, uses current season)
            target_date: The date to check (defaults to today)
            
        Returns:
            Dictionary with season information
        """
        if target_date is None:
            target_date = date.today()
        
        if season_year is None:
            season_year = self.get_current_season(sport, target_date)
        
        if sport not in self.seasons_data["seasons"]:
            raise ValueError(f"Unknown sport: {sport}")
        
        if season_year not in self.seasons_data["seasons"][sport]:
            raise ValueError(f"Unknown season {season_year} for {sport}")
        
        season_data = self.seasons_data["seasons"][sport][season_year]
        
        # Convert string dates to date objects
        pre_season_start = datetime.strptime(season_data["pre_season_start"], "%Y-%m-%d").date()
        regular_season_start = datetime.strptime(season_data["regular_season_start"], "%Y-%m-%d").date()
        regular_season_end = datetime.strptime(season_data["regular_season_end"], "%Y-%m-%d").date()
        playoffs_start = datetime.strptime(season_data["playoffs_start"], "%Y-%m-%d").date()
        playoffs_end = datetime.strptime(season_data["playoffs_end"], "%Y-%m-%d").date()
        
        # Determine season phase
        if target_date < pre_season_start:
            phase = "Off Season"
            week = None
        elif target_date < regular_season_start:
            phase = "Pre Season"
            days_into_pre = (target_date - pre_season_start).days
            week = max(1, (days_into_pre // 7) + 1)
        elif target_date <= regular_season_end:
            phase = "Regular Season"
            days_into_season = (target_date - regular_season_start).days
            week = max(1, (days_into_season // 7) + 1)
        elif target_date <= playoffs_end:
            phase = "Playoffs"
            days_into_playoffs = (target_date - playoffs_start).days
            week = max(1, (days_into_playoffs // 7) + 1)
        else:
            phase = "Off Season"
            week = None
        
        return {
            "sport": sport,
            "season_year": season_year,
            "name": season_data["name"],
            "phase": phase,
            "week": week,
            "api_base": season_data["api_base"],
            "dates": {
                "pre_season_start": pre_season_start,
                "regular_season_start": regular_season_start,
                "regular_season_end": regular_season_end,
                "playoffs_start": playoffs_start,
                "playoffs_end": playoffs_end
            }
        }
    
    def get_available_seasons(self, sport: str) -> List[str]:
        """Get list of available seasons for a sport."""
        if sport not in self.seasons_data["seasons"]:
            return []
        return list(self.seasons_data["seasons"][sport].keys())
    
    def add_season(self, sport: str, season_year: str, season_data: Dict[str, Any]) -> None:
        """Add a new season for a sport."""
        if sport not in self.seasons_data["seasons"]:
            self.seasons_data["seasons"][sport] = {}
        
        self.seasons_data["seasons"][sport][season_year] = season_data
        self._save_seasons_data(self.seasons_data)
    
    def update_season(self, sport: str, season_year: str, season_data: Dict[str, Any]) -> None:
        """Update an existing season."""
        if sport not in self.seasons_data["seasons"]:
            raise ValueError(f"Unknown sport: {sport}")
        
        if season_year not in self.seasons_data["seasons"][sport]:
            raise ValueError(f"Unknown season {season_year} for {sport}")
        
        self.seasons_data["seasons"][sport][season_year].update(season_data)
        self._save_seasons_data(self.seasons_data)
    
    def get_season_transition_info(self, sport: str) -> Dict[str, Any]:
        """Get information about upcoming season transitions."""
        current_date = date.today()
        current_season = self.get_current_season(sport, current_date)
        available_seasons = self.get_available_seasons(sport)
        
        # Find next season
        next_season = None
        for season in sorted(available_seasons):
            if season > current_season:
                next_season = season
                break
        
        info = {
            "current_season": current_season,
            "current_season_info": self.get_season_info(sport, current_season, current_date),
            "next_season": next_season,
            "available_seasons": available_seasons
        }
        
        if next_season:
            info["next_season_info"] = self.get_season_info(sport, next_season, current_date)
        
        return info


# Global season manager instance
season_manager = SeasonManager()


def get_current_season(sport: str, target_date: Optional[date] = None) -> str:
    """Get the current season year for a sport."""
    return season_manager.get_current_season(sport, target_date)


def get_season_info(sport: str, season_year: Optional[str] = None, 
                   target_date: Optional[date] = None) -> Dict[str, Any]:
    """Get season information for a sport and season."""
    return season_manager.get_season_info(sport, season_year, target_date)


def get_available_seasons(sport: str) -> List[str]:
    """Get list of available seasons for a sport."""
    return season_manager.get_available_seasons(sport)


def main():
    """Test the season manager."""
    print("Dynamic Season Manager Test")
    print("=" * 40)
    
    sports = ["wnba", "nba", "nhl", "mlb", "nfl"]
    current_date = date.today()
    
    for sport in sports:
        print(f"\n{sport.upper()}:")
        try:
            current_season = get_current_season(sport, current_date)
            season_info = get_season_info(sport, current_season, current_date)
            available_seasons = get_available_seasons(sport)
            
            print(f"  Current season: {current_season}")
            print(f"  Season name: {season_info['name']}")
            print(f"  Current phase: {season_info['phase']}")
            if season_info['week']:
                print(f"  Current week: {season_info['week']}")
            print(f"  Available seasons: {', '.join(available_seasons)}")
            
        except Exception as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    main() 