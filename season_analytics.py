#!/usr/bin/env python3
"""
Season Analytics Dashboard.

Provides insights into season progress, trends, and predictions.
"""

import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
from season_manager import SeasonManager, get_current_season, get_season_info, get_available_seasons


class SeasonAnalytics:
    """Analytics for sports seasons."""
    
    def __init__(self):
        """Initialize the analytics engine."""
        self.season_manager = SeasonManager()
    
    def get_season_progress(self, sport: str, season_year: Optional[str] = None) -> Dict:
        """
        Get detailed progress information for a season.
        
        Args:
            sport: The sport abbreviation
            season_year: The season year (if None, uses current season)
            
        Returns:
            Dictionary with progress information
        """
        if season_year is None:
            season_year = get_current_season(sport)
        
        season_info = get_season_info(sport, season_year)
        dates = season_info['dates']
        current_date = date.today()
        
        # Calculate progress percentages
        total_season_days = (dates['playoffs_end'] - dates['pre_season_start']).days
        days_elapsed = (current_date - dates['pre_season_start']).days
        progress_percentage = min(100, max(0, (days_elapsed / total_season_days) * 100))
        
        # Calculate phase progress
        phase_progress = self._calculate_phase_progress(season_info, current_date)
        
        # Calculate time until next phase
        next_phase_info = self._get_next_phase_info(season_info, current_date)
        
        return {
            'sport': sport,
            'season_year': season_year,
            'season_name': season_info['name'],
            'current_phase': season_info['phase'],
            'current_week': season_info['week'],
            'overall_progress': progress_percentage,
            'phase_progress': phase_progress,
            'next_phase': next_phase_info,
            'days_elapsed': days_elapsed,
            'total_days': total_season_days,
            'days_remaining': total_season_days - days_elapsed
        }
    
    def _calculate_phase_progress(self, season_info: Dict, current_date: date) -> Dict:
        """Calculate progress within the current phase."""
        dates = season_info['dates']
        current_phase = season_info['phase']
        
        if current_phase == "Off Season":
            return {'percentage': 0, 'days_elapsed': 0, 'total_days': 0}
        
        phase_start = None
        phase_end = None
        
        if current_phase == "Pre Season":
            phase_start = dates['pre_season_start']
            phase_end = dates['regular_season_start']
        elif current_phase == "Regular Season":
            phase_start = dates['regular_season_start']
            phase_end = dates['regular_season_end']
        elif current_phase == "Playoffs":
            phase_start = dates['playoffs_start']
            phase_end = dates['playoffs_end']
        
        if phase_start and phase_end:
            phase_days = (phase_end - phase_start).days
            days_elapsed = (current_date - phase_start).days
            percentage = min(100, max(0, (days_elapsed / phase_days) * 100))
            
            return {
                'percentage': percentage,
                'days_elapsed': days_elapsed,
                'total_days': phase_days,
                'days_remaining': phase_days - days_elapsed
            }
        
        return {'percentage': 0, 'days_elapsed': 0, 'total_days': 0}
    
    def _get_next_phase_info(self, season_info: Dict, current_date: date) -> Optional[Dict]:
        """Get information about the next phase."""
        dates = season_info['dates']
        current_phase = season_info['phase']
        
        if current_phase == "Off Season":
            next_phase = "Pre Season"
            next_start = dates['pre_season_start']
        elif current_phase == "Pre Season":
            next_phase = "Regular Season"
            next_start = dates['regular_season_start']
        elif current_phase == "Regular Season":
            next_phase = "Playoffs"
            next_start = dates['playoffs_start']
        elif current_phase == "Playoffs":
            next_phase = "Off Season"
            next_start = dates['playoffs_end']
        else:
            return None
        
        days_until_next = (next_start - current_date).days
        
        return {
            'phase': next_phase,
            'start_date': next_start,
            'days_until': days_until_next
        }
    
    def get_season_comparison(self, sport: str) -> Dict:
        """Compare multiple seasons for a sport."""
        available_seasons = get_available_seasons(sport)
        comparison = {}
        
        for season_year in available_seasons:
            try:
                progress = self.get_season_progress(sport, season_year)
                comparison[season_year] = progress
            except Exception as e:
                comparison[season_year] = {'error': str(e)}
        
        return comparison
    
    def get_cross_sport_analysis(self) -> Dict:
        """Get analysis across all sports."""
        sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
        analysis = {}
        
        for sport in sports:
            try:
                progress = self.get_season_progress(sport)
                analysis[sport] = progress
            except Exception as e:
                analysis[sport] = {'error': str(e)}
        
        return analysis
    
    def get_season_predictions(self, sport: str, season_year: Optional[str] = None) -> Dict:
        """Get predictions for season milestones."""
        if season_year is None:
            season_year = get_current_season(sport)
        
        season_info = get_season_info(sport, season_year)
        dates = season_info['dates']
        current_date = date.today()
        
        predictions = {
            'sport': sport,
            'season_year': season_year,
            'milestones': []
        }
        
        # Calculate upcoming milestones
        milestones = [
            ('Pre-season starts', dates['pre_season_start']),
            ('Regular season starts', dates['regular_season_start']),
            ('Regular season ends', dates['regular_season_end']),
            ('Playoffs start', dates['playoffs_start']),
            ('Playoffs end', dates['playoffs_end'])
        ]
        
        for milestone_name, milestone_date in milestones:
            days_until = (milestone_date - current_date).days
            status = 'completed' if milestone_date < current_date else 'upcoming' if days_until > 0 else 'today'
            
            predictions['milestones'].append({
                'name': milestone_name,
                'date': milestone_date,
                'days_until': days_until,
                'status': status
            })
        
        return predictions
    
    def generate_season_report(self, sport: str, season_year: Optional[str] = None) -> str:
        """Generate a comprehensive season report."""
        if season_year is None:
            season_year = get_current_season(sport)
        
        progress = self.get_season_progress(sport, season_year)
        predictions = self.get_season_predictions(sport, season_year)
        
        report_lines = []
        report_lines.append(f"📊 {sport.upper()} {season_year} SEASON REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Season: {progress['season_name']}")
        report_lines.append(f"Current Phase: {progress['current_phase']}")
        if progress['current_week']:
            report_lines.append(f"Current Week: {progress['current_week']}")
        report_lines.append("")
        
        # Progress bars
        report_lines.append("📈 PROGRESS:")
        report_lines.append(f"Overall Season: {progress['overall_progress']:.1f}%")
        if progress['phase_progress']['total_days'] > 0:
            phase_pct = progress['phase_progress']['percentage']
            report_lines.append(f"Current Phase: {phase_pct:.1f}%")
        report_lines.append("")
        
        # Time information
        report_lines.append("⏰ TIME:")
        report_lines.append(f"Days Elapsed: {progress['days_elapsed']}")
        report_lines.append(f"Days Remaining: {progress['days_remaining']}")
        if progress['next_phase']:
            next_phase = progress['next_phase']
            report_lines.append(f"Next Phase: {next_phase['phase']} (in {next_phase['days_until']} days)")
        report_lines.append("")
        
        # Milestones
        report_lines.append("🎯 MILESTONES:")
        for milestone in predictions['milestones']:
            if milestone['status'] == 'completed':
                status_icon = "✅"
            elif milestone['status'] == 'today':
                status_icon = "🎯"
            else:
                status_icon = "⏳"
            
            report_lines.append(f"{status_icon} {milestone['name']}: {milestone['date']}")
            if milestone['status'] == 'upcoming':
                report_lines.append(f"   → {milestone['days_until']} days until this milestone")
        
        return "\n".join(report_lines)


def main():
    """Test the season analytics."""
    print("Season Analytics Dashboard")
    print("=" * 40)
    
    analytics = SeasonAnalytics()
    
    # Test with WNBA
    print("\n📊 WNBA 2025 Season Analysis:")
    print("-" * 30)
    
    try:
        progress = analytics.get_season_progress('wnba', '2025')
        print(f"Sport: {progress['sport'].upper()}")
        print(f"Season: {progress['season_name']}")
        print(f"Current Phase: {progress['current_phase']}")
        print(f"Overall Progress: {progress['overall_progress']:.1f}%")
        print(f"Phase Progress: {progress['phase_progress']['percentage']:.1f}%")
        print(f"Days Elapsed: {progress['days_elapsed']}")
        print(f"Days Remaining: {progress['days_remaining']}")
        
        if progress['next_phase']:
            next_phase = progress['next_phase']
            print(f"Next Phase: {next_phase['phase']} (in {next_phase['days_until']} days)")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Generate full report
    print("\n📋 Full Season Report:")
    print("-" * 30)
    try:
        report = analytics.generate_season_report('wnba', '2025')
        print(report)
    except Exception as e:
        print(f"Error generating report: {e}")
    
    # Cross-sport analysis
    print("\n🌐 Cross-Sport Analysis:")
    print("-" * 30)
    analysis = analytics.get_cross_sport_analysis()
    
    for sport, data in analysis.items():
        if 'error' not in data:
            print(f"{sport.upper()}: {data['current_phase']} - {data['overall_progress']:.1f}% complete")
        else:
            print(f"{sport.upper()}: Error - {data['error']}")


if __name__ == "__main__":
    main() 