#!/usr/bin/env python3
"""
WNBA 2025 Season Date Management Module.

This module provides functions to manage and calculate WNBA season dates,
week numbers, and season phases for the 2025 season.
"""

from datetime import datetime, date
from typing import Dict, List, Tuple, Optional


class WNBADates2025:
    """WNBA 2025 Season date constants and calculations."""
    
    # Season dates for 2025
    PRE_SEASON_START = date(2025, 5, 2)
    REGULAR_SEASON_START = date(2025, 5, 16)
    COMMISSIONERS_CUP_START = date(2025, 6, 1)
    COMMISSIONERS_CUP_END = date(2025, 6, 17)
    ALL_STAR_BREAK_START = date(2025, 7, 17)
    ALL_STAR_GAME = date(2025, 7, 19)
    ALL_STAR_BREAK_END = date(2025, 7, 21)
    REGULAR_SEASON_END = date(2025, 9, 11)
    PLAYOFFS_START = date(2025, 9, 14)
    PLAYOFFS_END = date(2025, 10, 19)
    
    @classmethod
    def get_season_phases(cls) -> Dict[str, Dict[str, date]]:
        """
        Get all season phases with their start and end dates.
        
        Returns:
            Dict containing season phases with start and end dates.
        """
        return {
            "Pre-Season": {
                "start": cls.PRE_SEASON_START,
                "end": cls.REGULAR_SEASON_START - date.resolution
            },
            "Regular Season": {
                "start": cls.REGULAR_SEASON_START,
                "end": cls.REGULAR_SEASON_END
            },
            "Commissioner's Cup": {
                "start": cls.COMMISSIONERS_CUP_START,
                "end": cls.COMMISSIONERS_CUP_END
            },
            "All-Star Break": {
                "start": cls.ALL_STAR_BREAK_START,
                "end": cls.ALL_STAR_BREAK_END
            },
            "Playoffs": {
                "start": cls.PLAYOFFS_START,
                "end": cls.PLAYOFFS_END
            }
        }
    
    @classmethod
    def get_current_phase(cls, current_date: Optional[date] = None) -> Tuple[str, Optional[int]]:
        """
        Determine the current season phase and week number.
        
        Args:
            current_date: The date to check. Defaults to today.
            
        Returns:
            Tuple of (phase_name, week_number). Week number is None for off-season.
        """
        if current_date is None:
            current_date = date.today()
            
        phases = cls.get_season_phases()
        
        for phase_name, phase_dates in phases.items():
            if phase_dates["start"] <= current_date <= phase_dates["end"]:
                if phase_name == "Regular Season":
                    week_num = cls.calculate_regular_season_week(current_date)
                    return phase_name, week_num
                elif phase_name == "Pre-Season":
                    week_num = cls.calculate_pre_season_week(current_date)
                    return phase_name, week_num
                elif phase_name == "Playoffs":
                    week_num = cls.calculate_playoff_week(current_date)
                    return phase_name, week_num
                else:
                    return phase_name, None
        
        return "Off Season", None
    
    @classmethod
    def calculate_regular_season_week(cls, current_date: date) -> int:
        """
        Calculate the week number in the regular season.
        
        Args:
            current_date: The current date.
            
        Returns:
            Week number in the regular season (1-based).
        """
        days_elapsed = (current_date - cls.REGULAR_SEASON_START).days
        return (days_elapsed // 7) + 1
    
    @classmethod
    def calculate_pre_season_week(cls, current_date: date) -> int:
        """
        Calculate the week number in the pre-season.
        
        Args:
            current_date: The current date.
            
        Returns:
            Week number in the pre-season (1-based).
        """
        days_elapsed = (current_date - cls.PRE_SEASON_START).days
        return (days_elapsed // 7) + 1
    
    @classmethod
    def calculate_playoff_week(cls, current_date: date) -> int:
        """
        Calculate the week number in the playoffs.
        
        Args:
            current_date: The current date.
            
        Returns:
            Week number in the playoffs (1-based).
        """
        days_elapsed = (current_date - cls.PLAYOFFS_START).days
        return (days_elapsed // 7) + 1
    
    @classmethod
    def is_regular_season(cls, current_date: Optional[date] = None) -> bool:
        """
        Check if the current date is during the regular season.
        
        Args:
            current_date: The date to check. Defaults to today.
            
        Returns:
            True if during regular season, False otherwise.
        """
        if current_date is None:
            current_date = date.today()
            
        return cls.REGULAR_SEASON_START <= current_date <= cls.REGULAR_SEASON_END
    
    @classmethod
    def get_season_summary(cls) -> List[str]:
        """
        Get a formatted summary of all season dates.
        
        Returns:
            List of formatted date strings.
        """
        summary = [
            "WNBA 2025 Season Schedule:",
            "=" * 30,
            f"Pre-season start: {cls.PRE_SEASON_START.strftime('%B %d, %Y')}",
            f"Regular season start: {cls.REGULAR_SEASON_START.strftime('%B %d, %Y')}",
            f"Commissioner's Cup: {cls.COMMISSIONERS_CUP_START.strftime('%B %d')} - {cls.COMMISSIONERS_CUP_END.strftime('%B %d, %Y')}",
            f"All-Star Break: {cls.ALL_STAR_BREAK_START.strftime('%B %d')} - {cls.ALL_STAR_BREAK_END.strftime('%B %d, %Y')}",
            f"All-Star Game: {cls.ALL_STAR_GAME.strftime('%B %d, %Y')}",
            f"Regular season end: {cls.REGULAR_SEASON_END.strftime('%B %d, %Y')}",
            f"Playoffs start: {cls.PLAYOFFS_START.strftime('%B %d, %Y')}",
            f"Playoffs end: {cls.PLAYOFFS_END.strftime('%B %d, %Y')}"
        ]
        return summary


def main():
    """Display WNBA 2025 season information."""
    print("\n".join(WNBADates2025.get_season_summary()))
    
    current_phase, week_num = WNBADates2025.get_current_phase()
    print(f"\nCurrent phase: {current_phase}")
    if week_num:
        print(f"Current week: {week_num}")
    else:
        print("No week number available for current phase.")


if __name__ == "__main__":
    main() 