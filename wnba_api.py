#!/usr/bin/env python3
"""
WNBA API Server.

Provides both human-readable curl endpoints and JSON API endpoints for WNBA data.
"""

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

# Flask app for curl endpoints
app = Flask(__name__)

# FastAPI app for JSON endpoints
fastapi_app = FastAPI(
    title="WNBA API",
    description="API for WNBA standings, scores, and schedule data",
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

# FastAPI routes for JSON endpoints
@fastapi_app.get("/api/standings", response_model=StandingsResponse)
async def api_standings(group: str = "conference"):
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
        standings_lines = get_wnba_standings(json_data, group)
        # Parse standings into structured data
        eastern = []
        western = []
        league_wide = []
        current_conference = None
        for line in standings_lines:
            line = line.strip()
            if not line:
                continue
            if line.endswith(":"):
                current_conference = line.replace(":", "")
                continue
            try:
                parts = line.split()
                if len(parts) >= 6 and parts[2] == "-" and parts[4] == "GB:":
                    team_abbr = parts[0]
                    wins = int(parts[1])
                    losses = int(parts[3])
                    games_behind = float(parts[5])
                    entry = StandingsEntry(
                        team=team_abbr,
                        abbreviation=team_abbr,
                        wins=wins,
                        losses=losses,
                        games_behind=games_behind,
                        conference=current_conference or "Unknown"
                    )
                    if group == "league":
                        league_wide.append(entry)
                    else:
                        if "Eastern" in (current_conference or ""):
                            eastern.append(entry)
                        elif "Western" in (current_conference or ""):
                            western.append(entry)
            except (ValueError, IndexError) as e:
                print(f"DEBUG: Failed to parse line: {line} Error: {e}")
                continue
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

@fastapi_app.get("/api/scores", response_model=ScoresResponse)
async def api_scores(target_date: Optional[str] = None):
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

@fastapi_app.get("/api/schedule", response_model=ScheduleResponse)
async def api_schedule(target_date: Optional[str] = None):
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

# Mount FastAPI app under Flask
@app.route('/api/<path:path>')
def api_proxy(path):
    """Proxy FastAPI requests through Flask."""
    # This is a simplified proxy - in production you'd want a proper ASGI server
    return "FastAPI endpoints available at /api/standings, /api/scores, /api/schedule"

if __name__ == '__main__':
    print("Starting WNBA API Server...")
    print("Flask endpoints (curl-style):")
    print("  - http://localhost:5001/curl/help")
    print("  - http://localhost:5001/curl/standings")
    print("  - http://localhost:5001/curl/scores")
    print("  - http://localhost:5001/curl/schedule")
    print("\nFastAPI endpoints (JSON):")
    print("  - http://localhost:8001/api/standings")
    print("  - http://localhost:8001/api/scores")
    print("  - http://localhost:8001/api/schedule")
    print("  - http://localhost:8001/docs (OpenAPI docs)")
    
    # Start both servers
    import threading
    
    def run_fastapi():
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8001)
    
    def run_flask():
        app.run(host="0.0.0.0", port=5001, debug=False)
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Start Flask in main thread
    run_flask() 