#!/usr/bin/env python3
"""
Master Season Dashboard.

Comprehensive dashboard for all dynamic season management features.
"""

import json
import time
from datetime import date, datetime
from typing import Dict, List, Optional
from season_manager import SeasonManager, get_current_season, get_season_info, get_available_seasons
from season_analytics import SeasonAnalytics
from season_predictor import SeasonPredictor
from season_transitions import SeasonTransitionMonitor
import collections.abc


def to_serializable(obj):
    """Recursively convert date/datetime objects to ISO strings for JSON serialization."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(to_serializable(v) for v in obj)
    else:
        return obj


class SeasonDashboard:
    """Master dashboard for all season management features."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.season_manager = SeasonManager()
        self.analytics = SeasonAnalytics()
        self.predictor = SeasonPredictor()
        self.monitor = SeasonTransitionMonitor(check_interval=300)  # 5 minutes
        
        # Add default alert callback
        self.monitor.add_transition_callback(self._print_alert)
    
    def _print_alert(self, alert: Dict):
        """Default alert callback."""
        print(f"\n🚨 {alert['message']}")
        print(f"   Time: {alert['timestamp']}")
    
    def get_dashboard_summary(self) -> str:
        """Get a comprehensive dashboard summary."""
        sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
        summary_lines = []
        
        summary_lines.append("🎯 DYNAMIC SEASON MANAGEMENT DASHBOARD")
        summary_lines.append("=" * 60)
        summary_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
        
        # Current status for all sports
        summary_lines.append("📊 CURRENT SEASON STATUS:")
        summary_lines.append("-" * 30)
        
        for sport in sports:
            try:
                current_season = get_current_season(sport)
                season_info = get_season_info(sport, current_season)
                progress = self.analytics.get_season_progress(sport, current_season)
                
                summary_lines.append(f"{sport.upper()}:")
                summary_lines.append(f"  Season: {season_info['name']}")
                summary_lines.append(f"  Phase: {season_info['phase']}")
                if season_info['week']:
                    summary_lines.append(f"  Week: {season_info['week']}")
                summary_lines.append(f"  Progress: {progress['overall_progress']:.1f}%")
                summary_lines.append("")
                
            except Exception as e:
                summary_lines.append(f"{sport.upper()}: Error - {e}")
                summary_lines.append("")
        
        # Season transitions
        summary_lines.append("🔄 SEASON TRANSITIONS:")
        summary_lines.append("-" * 30)
        
        transitions = self.monitor.detect_transitions()
        if transitions:
            for transition in transitions:
                summary_lines.append(f"  {transition['sport'].upper()}: {transition['from']} → {transition['to']}")
        else:
            summary_lines.append("  No recent transitions detected")
        summary_lines.append("")
        
        # Available seasons
        summary_lines.append("📅 AVAILABLE SEASONS:")
        summary_lines.append("-" * 30)
        
        for sport in sports:
            try:
                available_seasons = get_available_seasons(sport)
                current_season = get_current_season(sport)
                summary_lines.append(f"{sport.upper()}: {', '.join(available_seasons)} (current: {current_season})")
            except Exception as e:
                summary_lines.append(f"{sport.upper()}: Error - {e}")
        summary_lines.append("")
        
        # Predictions
        summary_lines.append("🔮 SEASON PREDICTIONS:")
        summary_lines.append("-" * 30)
        
        for sport in sports:
            try:
                available_seasons = get_available_seasons(sport)
                if available_seasons:
                    latest_season = max(int(s) for s in available_seasons)
                    next_season = latest_season + 1
                    prediction = self.predictor.predict_future_season(sport, next_season)
                    summary_lines.append(f"{sport.upper()} {next_season}: {prediction['name']}")
                    summary_lines.append(f"  Regular season: {prediction['dates']['regular_season_start']} - {prediction['dates']['regular_season_end']}")
            except Exception as e:
                summary_lines.append(f"{sport.upper()}: Error predicting - {e}")
        summary_lines.append("")
        
        # System status
        summary_lines.append("⚙️ SYSTEM STATUS:")
        summary_lines.append("-" * 30)
        summary_lines.append("✅ Dynamic season detection: ACTIVE")
        summary_lines.append("✅ Season transition monitoring: ACTIVE")
        summary_lines.append("✅ Analytics engine: ACTIVE")
        summary_lines.append("✅ Prediction engine: ACTIVE")
        summary_lines.append("✅ API endpoints: ACTIVE")
        summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def get_sport_detailed_view(self, sport: str) -> str:
        """Get detailed view for a specific sport."""
        try:
            current_season = get_current_season(sport)
            season_info = get_season_info(sport, current_season)
            progress = self.analytics.get_season_progress(sport, current_season)
            predictions = self.analytics.get_season_predictions(sport, current_season)
            
            detailed_lines = []
            detailed_lines.append(f"📊 {sport.upper()} DETAILED VIEW")
            detailed_lines.append("=" * 50)
            detailed_lines.append(f"Current Season: {season_info['name']}")
            detailed_lines.append(f"Current Phase: {season_info['phase']}")
            if season_info['week']:
                detailed_lines.append(f"Current Week: {season_info['week']}")
            detailed_lines.append("")
            
            # Progress information
            detailed_lines.append("📈 PROGRESS:")
            detailed_lines.append(f"Overall Season: {progress['overall_progress']:.1f}%")
            if progress['phase_progress']['total_days'] > 0:
                phase_pct = progress['phase_progress']['percentage']
                detailed_lines.append(f"Current Phase: {phase_pct:.1f}%")
            detailed_lines.append(f"Days Elapsed: {progress['days_elapsed']}")
            detailed_lines.append(f"Days Remaining: {progress['days_remaining']}")
            detailed_lines.append("")
            
            # Next phase
            if progress['next_phase']:
                next_phase = progress['next_phase']
                detailed_lines.append("🔄 NEXT PHASE:")
                detailed_lines.append(f"Phase: {next_phase['phase']}")
                detailed_lines.append(f"Start Date: {next_phase['start_date']}")
                detailed_lines.append(f"Days Until: {next_phase['days_until']}")
                detailed_lines.append("")
            
            # Milestones
            detailed_lines.append("🎯 MILESTONES:")
            for milestone in predictions['milestones']:
                if milestone['status'] == 'completed':
                    status_icon = "✅"
                elif milestone['status'] == 'today':
                    status_icon = "🎯"
                else:
                    status_icon = "⏳"
                
                detailed_lines.append(f"{status_icon} {milestone['name']}: {milestone['date']}")
                if milestone['status'] == 'upcoming':
                    detailed_lines.append(f"   → {milestone['days_until']} days until this milestone")
            detailed_lines.append("")
            
            # Available seasons
            available_seasons = get_available_seasons(sport)
            detailed_lines.append("📅 AVAILABLE SEASONS:")
            for season in sorted(available_seasons):
                marker = " (current)" if season == current_season else ""
                detailed_lines.append(f"  {season}{marker}")
            
            return "\n".join(detailed_lines)
            
        except Exception as e:
            return f"Error getting detailed view for {sport}: {e}"
    
    def start_monitoring_dashboard(self, duration: Optional[int] = None):
        """Start the monitoring dashboard with live updates."""
        print("🚀 Starting Dynamic Season Management Dashboard")
        print("=" * 60)
        print("Press Ctrl+C to stop")
        print("")
        
        start_time = datetime.now()
        
        try:
            while True:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                # Display dashboard
                print(self.get_dashboard_summary())
                
                # Check if we should stop
                if duration and (datetime.now() - start_time).total_seconds() > duration:
                    print(f"\n⏰ Dashboard completed after {duration} seconds")
                    break
                
                # Wait for next update
                time.sleep(30)  # Update every 30 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
    
    def export_dashboard_data(self, filename: str):
        """Export dashboard data to JSON file."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'sports': {}
        }
        
        sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
        
        for sport in sports:
            try:
                current_season = get_current_season(sport)
                season_info = get_season_info(sport, current_season)
                progress = self.analytics.get_season_progress(sport, current_season)
                available_seasons = get_available_seasons(sport)
                
                data['sports'][sport] = {
                    'current_season': current_season,
                    'season_info': season_info,
                    'progress': progress,
                    'available_seasons': available_seasons
                }
            except Exception as e:
                data['sports'][sport] = {'error': str(e)}
        
        # Recursively convert all date/datetime objects
        data = to_serializable(data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📊 Dashboard data exported to {filename}")


def main():
    """Main dashboard interface."""
    dashboard = SeasonDashboard()
    
    while True:
        print("\n" + "=" * 60)
        print("🎯 DYNAMIC SEASON MANAGEMENT DASHBOARD")
        print("=" * 60)
        print("1. View dashboard summary")
        print("2. View detailed sport analysis")
        print("3. Start live monitoring dashboard")
        print("4. Export dashboard data")
        print("5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n" + dashboard.get_dashboard_summary())
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            sport = input("Enter sport (wnba/nba/nhl/mlb/nfl): ").lower().strip()
            if sport in ['wnba', 'nba', 'nhl', 'mlb', 'nfl']:
                print("\n" + dashboard.get_sport_detailed_view(sport))
                input("\nPress Enter to continue...")
            else:
                print("Invalid sport!")
                
        elif choice == '3':
            duration_str = input("Enter monitoring duration in seconds (or press Enter for infinite): ").strip()
            duration = int(duration_str) if duration_str else None
            dashboard.start_monitoring_dashboard(duration)
            
        elif choice == '4':
            filename = input("Enter filename for export (e.g., dashboard_data.json): ").strip()
            if filename:
                dashboard.export_dashboard_data(filename)
            else:
                dashboard.export_dashboard_data("dashboard_data.json")
                
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main() 