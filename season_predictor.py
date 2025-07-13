#!/usr/bin/env python3
"""
Season Prediction Engine.

Forecasts future seasons based on historical patterns and trends.
"""

import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
from season_manager import SeasonManager, get_available_seasons


class SeasonPredictor:
    """Predicts future seasons based on historical patterns."""
    
    def __init__(self):
        """Initialize the prediction engine."""
        self.season_manager = SeasonManager()
        
        # Historical season patterns (typical start/end dates)
        self.season_patterns = {
            'wnba': {
                'pre_season_start': {'month': 5, 'day': 2},
                'regular_season_start': {'month': 5, 'day': 16},
                'regular_season_end': {'month': 9, 'day': 11},
                'playoffs_start': {'month': 9, 'day': 14},
                'playoffs_end': {'month': 10, 'day': 19},
                'season_length_days': 170
            },
            'nba': {
                'pre_season_start': {'month': 10, 'day': 1},
                'regular_season_start': {'month': 10, 'day': 21},
                'regular_season_end': {'month': 4, 'day': 13},
                'playoffs_start': {'month': 4, 'day': 19},
                'playoffs_end': {'month': 6, 'day': 23},
                'season_length_days': 265
            },
            'nhl': {
                'pre_season_start': {'month': 9, 'day': 15},
                'regular_season_start': {'month': 10, 'day': 7},
                'regular_season_end': {'month': 4, 'day': 19},
                'playoffs_start': {'month': 4, 'day': 23},
                'playoffs_end': {'month': 6, 'day': 15},
                'season_length_days': 275
            },
            'mlb': {
                'pre_season_start': {'month': 2, 'day': 15},
                'regular_season_start': {'month': 3, 'day': 27},
                'regular_season_end': {'month': 9, 'day': 28},
                'playoffs_start': {'month': 10, 'day': 1},
                'playoffs_end': {'month': 11, 'day': 5},
                'season_length_days': 265
            },
            'nfl': {
                'pre_season_start': {'month': 8, 'day': 7},
                'regular_season_start': {'month': 9, 'day': 4},
                'regular_season_end': {'month': 1, 'day': 5},
                'playoffs_start': {'month': 1, 'day': 11},
                'playoffs_end': {'month': 2, 'day': 8},
                'season_length_days': 185
            }
        }
    
    def predict_future_season(self, sport: str, year: int) -> Dict:
        """
        Predict season dates for a future year.
        
        Args:
            sport: The sport abbreviation
            year: The year to predict for
            
        Returns:
            Dictionary with predicted season dates
        """
        if sport not in self.season_patterns:
            raise ValueError(f"Unknown sport: {sport}")
        
        pattern = self.season_patterns[sport]
        
        # Predict dates based on pattern
        predicted_dates = {}
        for phase, date_info in pattern.items():
            if phase != 'season_length_days':
                month = date_info['month']
                day = date_info['day']
                
                # Handle year transitions (e.g., NBA 2025-26 season)
                if sport in ['nba', 'nhl', 'nfl'] and month < 7:
                    # Season spans two years
                    season_year = year + 1
                else:
                    season_year = year
                
                predicted_dates[phase] = date(season_year, month, day)
        
        # Generate season name
        if sport in ['nba', 'nhl', 'nfl']:
            season_name = f"{sport.upper()} {year}-{year+1}"
        else:
            season_name = f"{sport.upper()} {year}"
        
        return {
            'sport': sport,
            'year': year,
            'name': season_name,
            'dates': predicted_dates,
            'api_base': f"https://api.sportsblaze.com/v1/{sport}",
            'prediction_confidence': 'high'
        }
    
    def predict_multiple_seasons(self, sport: str, start_year: int, num_seasons: int) -> List[Dict]:
        """
        Predict multiple future seasons.
        
        Args:
            sport: The sport abbreviation
            start_year: The first year to predict
            num_seasons: Number of seasons to predict
            
        Returns:
            List of predicted seasons
        """
        predictions = []
        
        for i in range(num_seasons):
            year = start_year + i
            try:
                prediction = self.predict_future_season(sport, year)
                predictions.append(prediction)
            except Exception as e:
                predictions.append({
                    'sport': sport,
                    'year': year,
                    'error': str(e)
                })
        
        return predictions
    
    def auto_add_future_seasons(self, sport: str, num_seasons: int = 3):
        """
        Automatically add predicted future seasons to the season manager.
        
        Args:
            sport: The sport abbreviation
            num_seasons: Number of future seasons to add
        """
        # Find the latest existing season
        available_seasons = get_available_seasons(sport)
        if not available_seasons:
            print(f"No existing seasons found for {sport}")
            return
        
        latest_season = max(int(s) for s in available_seasons)
        start_year = latest_season + 1
        
        print(f"Adding {num_seasons} future seasons for {sport.upper()} starting from {start_year}")
        
        predictions = self.predict_multiple_seasons(sport, start_year, num_seasons)
        
        for prediction in predictions:
            if 'error' not in prediction:
                try:
                    # Convert date objects to strings for storage
                    season_data = {
                        'name': prediction['name'],
                        'pre_season_start': prediction['dates']['pre_season_start'].strftime('%Y-%m-%d'),
                        'regular_season_start': prediction['dates']['regular_season_start'].strftime('%Y-%m-%d'),
                        'regular_season_end': prediction['dates']['regular_season_end'].strftime('%Y-%m-%d'),
                        'playoffs_start': prediction['dates']['playoffs_start'].strftime('%Y-%m-%d'),
                        'playoffs_end': prediction['dates']['playoffs_end'].strftime('%Y-%m-%d'),
                        'api_base': prediction['api_base']
                    }
                    
                    self.season_manager.add_season(sport, str(prediction['year']), season_data)
                    print(f"✅ Added {prediction['name']}")
                    
                except Exception as e:
                    print(f"❌ Error adding {prediction['name']}: {e}")
            else:
                print(f"❌ Error predicting {sport} {prediction['year']}: {prediction['error']}")
    
    def get_season_trends(self, sport: str) -> Dict:
        """
        Analyze trends in season dates over time.
        
        Args:
            sport: The sport abbreviation
            
        Returns:
            Dictionary with trend analysis
        """
        available_seasons = get_available_seasons(sport)
        if len(available_seasons) < 2:
            return {'error': 'Need at least 2 seasons for trend analysis'}
        
        trends = {
            'sport': sport,
            'seasons_analyzed': len(available_seasons),
            'trends': {}
        }
        
        # Analyze start date trends
        start_dates = []
        for season_year in sorted(available_seasons):
            try:
                season_info = self.season_manager.get_season_info(sport, season_year)
                start_dates.append({
                    'year': int(season_year),
                    'start_date': season_info['dates']['pre_season_start']
                })
            except Exception as e:
                continue
        
        if len(start_dates) >= 2:
            # Calculate average days between seasons
            date_diffs = []
            for i in range(1, len(start_dates)):
                diff = (start_dates[i]['start_date'] - start_dates[i-1]['start_date']).days
                date_diffs.append(diff)
            
            avg_diff = sum(date_diffs) / len(date_diffs)
            trends['trends']['avg_days_between_seasons'] = avg_diff
            trends['trends']['season_consistency'] = 'high' if max(date_diffs) - min(date_diffs) < 10 else 'medium'
        
        return trends
    
    def generate_season_forecast(self, sport: str, years_ahead: int = 5) -> str:
        """
        Generate a comprehensive season forecast.
        
        Args:
            sport: The sport abbreviation
            years_ahead: Number of years to forecast
            
        Returns:
            Formatted forecast string
        """
        available_seasons = get_available_seasons(sport)
        if not available_seasons:
            return f"No existing seasons found for {sport}"
        
        latest_season = max(int(s) for s in available_seasons)
        predictions = self.predict_multiple_seasons(sport, latest_season + 1, years_ahead)
        trends = self.get_season_trends(sport)
        
        forecast_lines = []
        forecast_lines.append(f"🔮 {sport.upper()} SEASON FORECAST")
        forecast_lines.append("=" * 50)
        forecast_lines.append(f"Current latest season: {latest_season}")
        forecast_lines.append(f"Forecasting {years_ahead} seasons ahead")
        forecast_lines.append("")
        
        if 'trends' in trends:
            forecast_lines.append("📊 TREND ANALYSIS:")
            if 'avg_days_between_seasons' in trends['trends']:
                avg_days = trends['trends']['avg_days_between_seasons']
                forecast_lines.append(f"Average days between seasons: {avg_days:.1f}")
            if 'season_consistency' in trends['trends']:
                consistency = trends['trends']['season_consistency']
                forecast_lines.append(f"Season consistency: {consistency}")
            forecast_lines.append("")
        
        forecast_lines.append("🎯 PREDICTED SEASONS:")
        for prediction in predictions:
            if 'error' not in prediction:
                forecast_lines.append(f"  {prediction['year']}: {prediction['name']}")
                forecast_lines.append(f"    Pre-season: {prediction['dates']['pre_season_start']}")
                forecast_lines.append(f"    Regular season: {prediction['dates']['regular_season_start']} - {prediction['dates']['regular_season_end']}")
                forecast_lines.append(f"    Playoffs: {prediction['dates']['playoffs_start']} - {prediction['dates']['playoffs_end']}")
                forecast_lines.append("")
            else:
                forecast_lines.append(f"  {prediction['year']}: Error - {prediction['error']}")
        
        return "\n".join(forecast_lines)


def main():
    """Test the season predictor."""
    print("Season Prediction Engine")
    print("=" * 40)
    
    predictor = SeasonPredictor()
    
    # Test prediction for WNBA
    print("\n🔮 WNBA 2027 Season Prediction:")
    print("-" * 30)
    
    try:
        prediction = predictor.predict_future_season('wnba', 2027)
        print(f"Sport: {prediction['sport'].upper()}")
        print(f"Season: {prediction['name']}")
        print(f"Pre-season start: {prediction['dates']['pre_season_start']}")
        print(f"Regular season: {prediction['dates']['regular_season_start']} - {prediction['dates']['regular_season_end']}")
        print(f"Playoffs: {prediction['dates']['playoffs_start']} - {prediction['dates']['playoffs_end']}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Generate forecast
    print("\n📋 WNBA Season Forecast:")
    print("-" * 30)
    try:
        forecast = predictor.generate_season_forecast('wnba', 3)
        print(forecast)
    except Exception as e:
        print(f"Error generating forecast: {e}")
    
    # Test auto-adding future seasons
    print("\n🚀 Auto-adding future seasons:")
    print("-" * 30)
    try:
        predictor.auto_add_future_seasons('wnba', 2)
    except Exception as e:
        print(f"Error auto-adding seasons: {e}")


if __name__ == "__main__":
    main() 