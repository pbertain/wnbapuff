#!/usr/bin/env python3
"""
WNBA API Server.

Provides both human-readable curl endpoints and JSON API endpoints for WNBA data.
"""

import argparse
from flask import Flask, request, jsonify
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import sys
import json
from datetime import date, datetime
from typing import Dict, Any, Optional, List
import uvicorn
from pydantic import BaseModel

# Import our existing scripts
from wnba_standings import fetch_wnba_data, get_wnba_standings
from wnba_scores import fetch_wnba_scores, format_event, get_status_display
from wnba_schedule import fetch_wnba_schedule, format_event as format_schedule_event
from wnba_dates import WNBADates2025

# Import new sports modules
from sports_api import fetch_sports_standings, fetch_sports_scores, fetch_sports_schedule, format_sports_standings
from sports_config import get_season_info

# Flask app for curl endpoints with static file support
app = Flask(__name__, static_folder='static', static_url_path='')

# FastAPI app for JSON endpoints
fastapi_app = FastAPI(
    title="SportsPuff Multi-Sport API",
    description="API for WNBA, NBA, NHL, MLB, and NFL standings, scores, and schedule data",
    version="1.0.0"
)

# Pydantic models for JSON responses
class Game(BaseModel):
    away_team: str
    home_team: str
    away_score: Optional[int] = None
    home_score: Optional[int] = None
    status: str
    away_record: Optional[str] = None
    home_record: Optional[str] = None

class StandingsEntry(BaseModel):
    team: str
    abbreviation: str
    wins: int
    losses: int
    games_behind: float
    conference: str

class StandingsResponse(BaseModel):
    eastern_conference: List[StandingsEntry]
    western_conference: List[StandingsEntry]
    league_wide: Optional[List[StandingsEntry]] = None
    season_phase: str
    week_number: Optional[int] = None

class ScoresResponse(BaseModel):
    games: List[Game]
    date: str
    season_phase: str
    week_number: Optional[int] = None

class ScheduleResponse(BaseModel):
    games: List[Game]
    date: str
    season_phase: str
    week_number: Optional[int] = None

# Helper functions
def run_script_output(script_name: str, args: Optional[List[str]] = None) -> str:
    """Run a Python script and return its output."""
    try:
        cmd = [sys.executable, script_name]
        if args:
            cmd.extend(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error running {script_name}: {result.stderr}"
    except subprocess.TimeoutExpired:
        return f"Error: {script_name} timed out"
    except Exception as e:
        return f"Error running {script_name}: {str(e)}"

def get_target_date() -> date:
    """Get target date from request parameters."""
    date_str = request.args.get('date')
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return date.today()
    return date.today()

# Flask routes for curl endpoints
@app.route('/curl/help')
def curl_help():
    """Display help information for curl endpoints."""
    help_text = """
WNBA API - Curl Endpoints
=========================

Available endpoints:
- /curl/help - Show this help message
- /curl/standings - Show current standings
- /curl/scores - Show today's scores
- /curl/schedule - Show today's schedule

Optional parameters:
- date: YYYY-MM-DD format (e.g., ?date=2025-07-09)
- group: "conference" or "league" (for standings only)
- timezone: Timezone name (e.g., ?timezone=America/New_York)

Examples:
- /curl/standings
- /curl/standings?group=league
- /curl/scores?date=2025-07-09
- /curl/schedule?timezone=America/New_York
"""
    return help_text

@app.route('/curl/standings')
def curl_standings():
    """Display standings in human-readable format."""
    group = request.args.get('group', 'conference')
    if group not in ['conference', 'league']:
        group = 'conference'
    
    # Run the standings script
    args = ['--group', group]
    output = run_script_output('wnba_standings.py', args)
    return output

@app.route('/curl/scores')
def curl_scores():
    """Display scores in human-readable format."""
    date_str = request.args.get('date')
    timezone = request.args.get('timezone', 'America/Los_Angeles')
    
    args = []
    if date_str:
        args.extend(['--date', date_str])
    if timezone:
        args.extend(['--timezone', timezone])
    
    output = run_script_output('wnba_scores.py', args)
    return output

@app.route('/curl/schedule')
def curl_schedule():
    """Display schedule in human-readable format."""
    date_str = request.args.get('date')
    timezone = request.args.get('timezone', 'America/Los_Angeles')
    
    args = []
    if date_str:
        args.extend(['--date', date_str])
    if timezone:
        args.extend(['--timezone', timezone])
    
    output = run_script_output('wnba_schedule.py', args)
    return output

# New /curl/wnba endpoints
@app.route('/curl/wnba/help')
def curl_wnba_help():
    """Display help information for /curl/wnba endpoints."""
    help_text = """
WNBA API - /curl/wnba Endpoints
==============================

Available endpoints:
- /curl/wnba/help - Show this help message
- /curl/wnba/standings - Show current standings
- /curl/wnba/scores - Show today's scores
- /curl/wnba/schedule - Show today's schedule

Optional parameters:
- date: YYYY-MM-DD format (e.g., ?date=2025-07-09)
- group: "conference" or "league" (for standings only)
- timezone: Timezone name (e.g., ?timezone=America/New_York)

Examples:
- /curl/wnba/standings
- /curl/wnba/standings?group=league
- /curl/wnba/scores?date=2025-07-09
- /curl/wnba/schedule?timezone=America/New_York
"""
    return help_text

@app.route('/curl/wnba/standings')
def curl_wnba_standings():
    """Display WNBA standings in human-readable format."""
    group = request.args.get('group', 'conference')
    if group not in ['conference', 'league']:
        group = 'conference'
    
    # Run the standings script
    args = ['--group', group]
    output = run_script_output('wnba_standings.py', args)
    return output

@app.route('/curl/wnba/scores')
def curl_wnba_scores():
    """Display WNBA scores in human-readable format."""
    date_str = request.args.get('date')
    timezone = request.args.get('timezone', 'America/Los_Angeles')
    
    args = []
    if date_str:
        args.extend(['--date', date_str])
    if timezone:
        args.extend(['--timezone', timezone])
    
    output = run_script_output('wnba_scores.py', args)
    return output

@app.route('/curl/wnba/schedule')
def curl_wnba_schedule():
    """Display WNBA schedule in human-readable format."""
    date_str = request.args.get('date')
    timezone = request.args.get('timezone', 'America/Los_Angeles')
    
    args = []
    if date_str:
        args.extend(['--date', date_str])
    if timezone:
        args.extend(['--timezone', timezone])
    
    output = run_script_output('wnba_schedule.py', args)
    return output

# Generic sports endpoints for all sports
def create_sports_endpoints(sport: str):
    """Create Flask endpoints for a specific sport."""
    
    @app.route(f'/curl/{sport}/help', endpoint=f'{sport}_help')
    def sports_help():
        """Display help information for sport endpoints."""
        help_text = f"""
{sport.upper()} API - Curl Endpoints
==============================

Available endpoints:
- /curl/{sport}/help - Show this help message
- /curl/{sport}/standings - Show current standings
- /curl/{sport}/scores - Show today's scores
- /curl/{sport}/schedule - Show today's schedule

Optional parameters:
- date: YYYY-MM-DD format (e.g., ?date=2025-07-09)
- season: Season year (e.g., ?season=2025)
- group: "conference" or "league" (for standings only)
- timezone: Timezone name (e.g., ?timezone=America/New_York)

Examples:
- /curl/{sport}/standings
- /curl/{sport}/standings?group=league&season=2025
- /curl/{sport}/scores?date=2025-07-09&season=2025
- /curl/{sport}/schedule?timezone=America/New_York&season=2026
"""
        return help_text

    @app.route(f'/curl/{sport}/standings', endpoint=f'{sport}_standings')
    def sports_standings():
        """Display sport standings in human-readable format."""
        group = request.args.get('group', 'conference')
        if group not in ['conference', 'league']:
            group = 'conference'
        
        season_year = request.args.get('season')
        
        # Fetch standings data
        json_data = fetch_sports_standings(sport, group, season_year)
        if not json_data:
            return f"Error fetching {sport.upper()} standings data."
        
        # Format standings
        output = format_sports_standings(json_data, sport, group, season_year)
        return output

    @app.route(f'/curl/{sport}/scores', endpoint=f'{sport}_scores')
    def sports_scores():
        """Display sport scores in human-readable format."""
        date_str = request.args.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                target_date = date.today()
        else:
            target_date = date.today()
        
        season_year = request.args.get('season')
        
        # Fetch scores data
        json_data = fetch_sports_scores(sport, target_date, season_year)
        if not json_data:
            return f"No {sport.upper()} games found for {target_date.strftime('%Y-%m-%d')}."
        
        # For now, return a simple message
        season_info = get_season_info(sport, target_date, season_year)
        return f"{sport.upper()} scores for {target_date.strftime('%Y-%m-%d')}:\nSeason: {season_info['name']} - {season_info['phase']}\n(Detailed formatting coming soon)"

    @app.route(f'/curl/{sport}/schedule', endpoint=f'{sport}_schedule')
    def sports_schedule():
        """Display sport schedule in human-readable format."""
        date_str = request.args.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                target_date = date.today()
        else:
            target_date = date.today()
        
        season_year = request.args.get('season')
        
        # Fetch schedule data
        json_data = fetch_sports_schedule(sport, target_date, season_year)
        if not json_data:
            return f"No {sport.upper()} games scheduled for {target_date.strftime('%Y-%m-%d')}."
        
        # For now, return a simple message
        season_info = get_season_info(sport, target_date, season_year)
        return f"{sport.upper()} schedule for {target_date.strftime('%Y-%m-%d')}:\nSeason: {season_info['name']} - {season_info['phase']}\n(Detailed formatting coming soon)"

# Create endpoints for all sports
create_sports_endpoints('nba')
create_sports_endpoints('nhl')
create_sports_endpoints('mlb')
create_sports_endpoints('nfl')

# FastAPI routes for JSON endpoints
@fastapi_app.get("/api/wnba/standings", response_model=StandingsResponse)
async def api_wnba_standings(group: str = "conference"):
    """Get standings data in JSON format."""
    if group not in ["conference", "league"]:
        raise HTTPException(status_code=400, detail="Group must be 'conference' or 'league'")
    
    # Get current phase and week
    current_phase, week_num = WNBADates2025.get_current_phase()
    
    # Fetch standings data
    json_data = fetch_wnba_data()
    
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to fetch standings data")
    
    # Process standings
    try:
        eastern = []
        western = []
        league_wide = []
        
        # Parse JSON data directly
        for conference in json_data.get('children', []):
            conference_name = conference['name']
            entries = conference.get('standings', {}).get('entries', [])
            
            for entry in entries:
                # Find wins, losses, and games behind stats
                wins_stat = None
                losses_stat = None
                games_behind_stat = None
                
                for stat in entry.get('stats', []):
                    if stat.get('name') == 'wins':
                        wins_stat = stat
                    elif stat.get('name') == 'losses':
                        losses_stat = stat
                    elif stat.get('name') == 'gamesBehind':
                        games_behind_stat = stat
                
                if wins_stat and losses_stat:
                    wins = int(wins_stat['value'])
                    losses = int(losses_stat['value'])
                    games_behind = float(games_behind_stat['value']) if games_behind_stat else 0.0
                    
                    team_info = entry['team']
                    team_abbr = team_info['abbreviation']
                    team_name = team_info['shortDisplayName']
                    
                    standings_entry = StandingsEntry(
                        team=team_name,
                        abbreviation=team_abbr,
                        wins=wins,
                        losses=losses,
                        games_behind=games_behind,
                        conference=conference_name
                    )
                    
                    if group == "league":
                        league_wide.append(standings_entry)
                    else:
                        if "Eastern" in conference_name:
                            eastern.append(standings_entry)
                        elif "Western" in conference_name:
                            western.append(standings_entry)
        return StandingsResponse(
            eastern_conference=eastern,
            western_conference=western,
            league_wide=league_wide if group == "league" else None,
            season_phase=current_phase,
            week_number=week_num
        )
    except Exception as e:
        import traceback
        print("DEBUG: Exception in api_standings:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@fastapi_app.get("/api/wnba/scores", response_model=ScoresResponse)
async def api_wnba_scores(target_date: Optional[str] = None):
    """Get scores data in JSON format."""
    # Parse date
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        parsed_date = date.today()
    
    # Get current phase and week
    current_phase, week_num = WNBADates2025.get_current_phase(parsed_date)
    
    # Fetch scores data
    scores_data = fetch_wnba_scores(parsed_date)
    
    if not scores_data:
        raise HTTPException(status_code=500, detail="Failed to fetch scores data")
    
    # Process games
    games = []
    events = scores_data.get('events', [])
    
    for event in events:
        try:
            competition = event['competitions'][0]
            competitors = competition['competitors']
            
            # Find home and away teams
            home_team = None
            away_team = None
            
            for competitor in competitors:
                if competitor.get('homeAway') == 'home':
                    home_team = competitor
                elif competitor.get('homeAway') == 'away':
                    away_team = competitor
            
            if not home_team or not away_team:
                continue
            
            # Get scores
            home_score = home_team.get('score', '0')
            away_score = away_team.get('score', '0')
            
            # Get status
            status = competition.get('status', {})
            status_type = status.get('type', {})
            status_name = status_type.get('name', 'Unknown')
            status_description = status_type.get('description', '')
            period = status.get('period', None)
            
            status_display = get_status_display(status_name, status_description, period)
            
            # Get records
            home_record = home_team.get('records', [{}])[0].get('summary', '')
            away_record = away_team.get('records', [{}])[0].get('summary', '')
            
            game = Game(
                away_team=away_team['team']['abbreviation'],
                home_team=home_team['team']['abbreviation'],
                away_score=int(away_score) if away_score.isdigit() else None,
                home_score=int(home_score) if home_score.isdigit() else None,
                status=status_display,
                away_record=away_record if away_record else None,
                home_record=home_record if home_record else None
            )
            games.append(game)
            
        except Exception as e:
            continue  # Skip malformed games
    
    return ScoresResponse(
        games=games,
        date=parsed_date.strftime("%Y-%m-%d"),
        season_phase=current_phase,
        week_number=week_num
    )

@fastapi_app.get("/api/wnba/schedule", response_model=ScheduleResponse)
async def api_wnba_schedule(target_date: Optional[str] = None):
    """Get schedule data in JSON format."""
    # Parse date
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        parsed_date = date.today()
    
    # Get current phase and week
    current_phase, week_num = WNBADates2025.get_current_phase(parsed_date)
    
    # Fetch schedule data
    schedule_data = fetch_wnba_schedule(parsed_date)
    
    if not schedule_data:
        raise HTTPException(status_code=500, detail="Failed to fetch schedule data")
    
    # Process games (similar to scores but without scores)
    games = []
    events = schedule_data.get('events', [])
    
    for event in events:
        try:
            competition = event['competitions'][0]
            competitors = competition['competitors']
            
            # Find home and away teams
            home_team = None
            away_team = None
            
            for competitor in competitors:
                if competitor.get('homeAway') == 'home':
                    home_team = competitor
                elif competitor.get('homeAway') == 'away':
                    away_team = competitor
            
            if not home_team or not away_team:
                continue
            
            # Get records
            home_record = home_team.get('records', [{}])[0].get('summary', '')
            away_record = away_team.get('records', [{}])[0].get('summary', '')
            
            game = Game(
                away_team=away_team['team']['abbreviation'],
                home_team=home_team['team']['abbreviation'],
                status="Scheduled",
                away_record=away_record if away_record else None,
                home_record=home_record if home_record else None
            )
            games.append(game)
            
        except Exception as e:
            continue  # Skip malformed games
    
    return ScheduleResponse(
        games=games,
        date=parsed_date.strftime("%Y-%m-%d"),
        season_phase=current_phase,
        week_number=week_num
    )

# FastAPI endpoints for other sports
@fastapi_app.get("/api/nba/standings", response_model=StandingsResponse)
async def api_nba_standings(group: str = "conference"):
    """Get NBA standings data in JSON format."""
    if group not in ["conference", "league"]:
        raise HTTPException(status_code=400, detail="Group must be 'conference' or 'league'")
    
    # Get current phase and week
    season_info = get_season_info('nba')
    
    # Fetch standings data
    json_data = fetch_sports_standings('nba', group)
    
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to fetch NBA standings data")
    
    # For now, return a simple response
    return StandingsResponse(
        eastern_conference=[],
        western_conference=[],
        league_wide=None,
        season_phase=season_info['phase'],
        week_number=season_info['week']
    )

@fastapi_app.get("/api/nhl/standings", response_model=StandingsResponse)
async def api_nhl_standings(group: str = "conference"):
    """Get NHL standings data in JSON format."""
    if group not in ["conference", "league"]:
        raise HTTPException(status_code=400, detail="Group must be 'conference' or 'league'")
    
    # Get current phase and week
    season_info = get_season_info('nhl')
    
    # Fetch standings data
    json_data = fetch_sports_standings('nhl', group)
    
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to fetch NHL standings data")
    
    # For now, return a simple response
    return StandingsResponse(
        eastern_conference=[],
        western_conference=[],
        league_wide=None,
        season_phase=season_info['phase'],
        week_number=season_info['week']
    )

@fastapi_app.get("/api/mlb/standings", response_model=StandingsResponse)
async def api_mlb_standings(group: str = "conference"):
    """Get MLB standings data in JSON format."""
    if group not in ["conference", "league"]:
        raise HTTPException(status_code=400, detail="Group must be 'conference' or 'league'")
    
    # Get current phase and week
    season_info = get_season_info('mlb')
    
    # Fetch standings data
    json_data = fetch_sports_standings('mlb', group)
    
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to fetch MLB standings data")
    
    # For now, return a simple response
    return StandingsResponse(
        eastern_conference=[],
        western_conference=[],
        league_wide=None,
        season_phase=season_info['phase'],
        week_number=season_info['week']
    )

@fastapi_app.get("/api/nfl/standings", response_model=StandingsResponse)
async def api_nfl_standings(group: str = "conference"):
    """Get NFL standings data in JSON format."""
    if group not in ["conference", "league"]:
        raise HTTPException(status_code=400, detail="Group must be 'conference' or 'league'")
    
    # Get current phase and week
    season_info = get_season_info('nfl')
    
    # Fetch standings data
    json_data = fetch_sports_standings('nfl', group)
    
    if not json_data:
        raise HTTPException(status_code=500, detail="Failed to fetch NFL standings data")
    
    # For now, return a simple response
    return StandingsResponse(
        eastern_conference=[],
        western_conference=[],
        league_wide=None,
        season_phase=season_info['phase'],
        week_number=season_info['week']
    )

# Placeholder endpoints for other sports
@app.route('/api/mlb/<path:path>')
def mlb_proxy(path):
    """Placeholder for MLB endpoints."""
    return f"MLB API endpoint /api/mlb/{path} - Coming soon!"

@app.route('/api/nfl/<path:path>')
def nfl_proxy(path):
    """Placeholder for NFL endpoints."""
    return f"NFL API endpoint /api/nfl/{path} - Coming soon!"

@app.route('/api/nhl/<path:path>')
def nhl_proxy(path):
    """Placeholder for NHL endpoints."""
    return f"NHL API endpoint /api/nhl/{path} - Coming soon!"

@app.route('/api/nba/<path:path>')
def nba_proxy(path):
    """Placeholder for NBA endpoints."""
    return f"NBA API endpoint /api/nba/{path} - Coming soon!"

# Serve static files
@app.route('/')
def index():
    """Serve the main web interface."""
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.)."""
    return app.send_static_file(filename)

# Mount FastAPI app under Flask
@app.route('/api/wnba/<path:path>')
def wnba_api_proxy(path):
    """Proxy WNBA API requests to FastAPI server."""
    return f"WNBA API endpoint /api/wnba/{path} - Use port 8001 for JSON endpoints"

@app.route('/api/<path:path>')
def api_proxy(path):
    """Proxy other API requests through Flask."""
    # This is a simplified proxy - in production you'd want a proper ASGI server
    return "API endpoints available at /api/wnba/standings, /api/wnba/scores, /api/wnba/schedule"

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SportsPuff Multi-Sport API Server')
    parser.add_argument('--port', type=int, default=34081, 
                       help='Port for Flask server (default: 34081)')
    parser.add_argument('--fastapi-port', type=int, default=34080,
                       help='Port for FastAPI server (default: 34080)')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                       help='Host to bind to (default: 0.0.0.0)')
    
    args = parser.parse_args()
    
    print("Starting SportsPuff Multi-Sport API Server...")
    print(f"\nFlask endpoints (Human-readable) on port {args.port}:")
    print("WNBA:")
    print(f"  - http://localhost:{args.port}/curl/wnba/help")
    print(f"  - http://localhost:{args.port}/curl/wnba/standings")
    print(f"  - http://localhost:{args.port}/curl/wnba/scores")
    print(f"  - http://localhost:{args.port}/curl/wnba/schedule")
    print("\nNBA:")
    print(f"  - http://localhost:{args.port}/curl/nba/help")
    print(f"  - http://localhost:{args.port}/curl/nba/standings")
    print(f"  - http://localhost:{args.port}/curl/nba/scores")
    print(f"  - http://localhost:{args.port}/curl/nba/schedule")
    print("\nNHL:")
    print(f"  - http://localhost:{args.port}/curl/nhl/help")
    print(f"  - http://localhost:{args.port}/curl/nhl/standings")
    print(f"  - http://localhost:{args.port}/curl/nhl/scores")
    print(f"  - http://localhost:{args.port}/curl/nhl/schedule")
    print("\nMLB:")
    print(f"  - http://localhost:{args.port}/curl/mlb/help")
    print(f"  - http://localhost:{args.port}/curl/mlb/standings")
    print(f"  - http://localhost:{args.port}/curl/mlb/scores")
    print(f"  - http://localhost:{args.port}/curl/mlb/schedule")
    print("\nNFL:")
    print(f"  - http://localhost:{args.port}/curl/nfl/help")
    print(f"  - http://localhost:{args.port}/curl/nfl/standings")
    print(f"  - http://localhost:{args.port}/curl/nfl/scores")
    print(f"  - http://localhost:{args.port}/curl/nfl/schedule")
    print(f"\nFastAPI endpoints (JSON) on port {args.fastapi_port}:")
    print(f"  - http://localhost:{args.fastapi_port}/api/wnba/standings")
    print(f"  - http://localhost:{args.fastapi_port}/api/nba/standings")
    print(f"  - http://localhost:{args.fastapi_port}/api/nhl/standings")
    print(f"  - http://localhost:{args.fastapi_port}/api/mlb/standings")
    print(f"  - http://localhost:{args.fastapi_port}/api/nfl/standings")
    print(f"  - http://localhost:{args.fastapi_port}/docs (OpenAPI docs)")
    
    # Start both servers
    import threading
    
    def run_fastapi():
        uvicorn.run(fastapi_app, host=args.host, port=args.fastapi_port)
    
    def run_flask():
        app.run(host=args.host, port=args.port, debug=False)
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Start Flask in main thread
    run_flask() 