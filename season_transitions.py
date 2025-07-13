#!/usr/bin/env python3
"""
Season Transition Monitor.

Monitors season transitions and provides alerts when seasons change.
"""

import time
import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Callable
from season_manager import SeasonManager, get_current_season, get_season_info


class SeasonTransitionMonitor:
    """Monitors season transitions and provides alerts."""
    
    def __init__(self, check_interval: int = 3600):  # Check every hour
        """
        Initialize the season transition monitor.
        
        Args:
            check_interval: Seconds between checks
        """
        self.check_interval = check_interval
        self.season_manager = SeasonManager()
        self.last_states = {}
        self.transition_callbacks = []
        self.alert_history = []
        
    def add_transition_callback(self, callback: Callable):
        """Add a callback function to be called when season transitions occur."""
        self.transition_callbacks.append(callback)
    
    def get_current_states(self) -> Dict[str, Dict]:
        """Get current season states for all sports."""
        states = {}
        sports = ['wnba', 'nba', 'nhl', 'mlb', 'nfl']
        
        for sport in sports:
            try:
                current_season = get_current_season(sport)
                season_info = get_season_info(sport, current_season)
                states[sport] = {
                    'season': current_season,
                    'phase': season_info['phase'],
                    'week': season_info['week'],
                    'name': season_info['name']
                }
            except Exception as e:
                states[sport] = {'error': str(e)}
        
        return states
    
    def detect_transitions(self) -> List[Dict]:
        """Detect season transitions since last check."""
        current_states = self.get_current_states()
        transitions = []
        
        for sport, current_state in current_states.items():
            if sport not in self.last_states:
                # First time checking this sport
                self.last_states[sport] = current_state
                continue
            
            last_state = self.last_states[sport]
            
            # Check for season changes
            if current_state.get('season') != last_state.get('season'):
                transitions.append({
                    'sport': sport,
                    'type': 'season_change',
                    'from': last_state.get('season'),
                    'to': current_state.get('season'),
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check for phase changes
            elif current_state.get('phase') != last_state.get('phase'):
                transitions.append({
                    'sport': sport,
                    'type': 'phase_change',
                    'season': current_state.get('season'),
                    'from': last_state.get('phase'),
                    'to': current_state.get('phase'),
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check for week changes
            elif (current_state.get('week') != last_state.get('week') and 
                  current_state.get('week') is not None):
                transitions.append({
                    'sport': sport,
                    'type': 'week_change',
                    'season': current_state.get('season'),
                    'phase': current_state.get('phase'),
                    'from': last_state.get('week'),
                    'to': current_state.get('week'),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Update last states
        self.last_states = current_states
        
        return transitions
    
    def alert_transition(self, transition: Dict):
        """Generate an alert for a season transition."""
        alert = {
            'id': f"{transition['sport']}_{transition['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'transition': transition,
            'message': self._format_alert_message(transition),
            'timestamp': datetime.now().isoformat()
        }
        
        self.alert_history.append(alert)
        
        # Call transition callbacks
        for callback in self.transition_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Error in transition callback: {e}")
        
        return alert
    
    def _format_alert_message(self, transition: Dict) -> str:
        """Format a human-readable alert message."""
        sport = transition['sport'].upper()
        
        if transition['type'] == 'season_change':
            return f"🎉 {sport} SEASON TRANSITION: {transition['from']} → {transition['to']}"
        elif transition['type'] == 'phase_change':
            return f"🔄 {sport} PHASE CHANGE: {transition['from']} → {transition['to']} (Season {transition['season']})"
        elif transition['type'] == 'week_change':
            return f"📅 {sport} WEEK {transition['from']} → {transition['to']} ({transition['phase']}, Season {transition['season']})"
        else:
            return f"ℹ️ {sport} transition: {transition}"
    
    def start_monitoring(self, duration: Optional[int] = None):
        """
        Start monitoring season transitions.
        
        Args:
            duration: Duration to monitor in seconds (None for infinite)
        """
        print(f"🔍 Starting season transition monitoring (check every {self.check_interval} seconds)")
        print("Press Ctrl+C to stop")
        
        start_time = datetime.now()
        
        try:
            while True:
                # Detect transitions
                transitions = self.detect_transitions()
                
                # Alert on transitions
                for transition in transitions:
                    alert = self.alert_transition(transition)
                    print(f"\n🚨 {alert['message']}")
                    print(f"   Time: {alert['timestamp']}")
                
                # Check if we should stop
                if duration and (datetime.now() - start_time).total_seconds() > duration:
                    print(f"\n⏰ Monitoring completed after {duration} seconds")
                    break
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Season monitoring stopped by user")
    
    def get_alert_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get alert history."""
        if limit:
            return self.alert_history[-limit:]
        return self.alert_history
    
    def export_alerts(self, filename: str):
        """Export alert history to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.alert_history, f, indent=2)
        print(f"📊 Alerts exported to {filename}")


def print_alert(alert: Dict):
    """Default alert callback that prints to console."""
    print(f"\n{'='*60}")
    print(f"🚨 SEASON TRANSITION ALERT")
    print(f"{'='*60}")
    print(f"Sport: {alert['transition']['sport'].upper()}")
    print(f"Type: {alert['transition']['type']}")
    print(f"Message: {alert['message']}")
    print(f"Time: {alert['timestamp']}")
    print(f"{'='*60}")


def webhook_alert(webhook_url: str):
    """Create a webhook alert callback."""
    import requests
    
    def callback(alert: Dict):
        try:
            payload = {
                'text': alert['message'],
                'timestamp': alert['timestamp'],
                'transition': alert['transition']
            }
            requests.post(webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Webhook error: {e}")
    
    return callback


def main():
    """Test the season transition monitor."""
    print("Season Transition Monitor Test")
    print("=" * 40)
    
    # Create monitor
    monitor = SeasonTransitionMonitor(check_interval=60)  # Check every minute
    
    # Add alert callbacks
    monitor.add_transition_callback(print_alert)
    
    # Get current states
    print("\nCurrent season states:")
    states = monitor.get_current_states()
    for sport, state in states.items():
        if 'error' not in state:
            print(f"  {sport.upper()}: {state['name']} - {state['phase']}")
            if state['week']:
                print(f"    Week: {state['week']}")
        else:
            print(f"  {sport.upper()}: Error - {state['error']}")
    
    # Start monitoring
    print(f"\nStarting monitoring (will check every {monitor.check_interval} seconds)...")
    monitor.start_monitoring(duration=300)  # Monitor for 5 minutes
    
    # Show alert history
    alerts = monitor.get_alert_history()
    if alerts:
        print(f"\n📊 Alert History ({len(alerts)} alerts):")
        for alert in alerts[-5:]:  # Show last 5 alerts
            print(f"  {alert['timestamp']}: {alert['message']}")
    else:
        print("\n📊 No transitions detected during monitoring period")


if __name__ == "__main__":
    main() 