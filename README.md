# WNBA Standings Fetcher

A Python script to fetch and display WNBA standings for the 2025 season with accurate date calculations and season phase detection.

## Features

- **Accurate 2025 Season Dates**: Uses correct WNBA 2025 season dates for all calculations
- **Modular Design**: Separate `wnba_dates.py` module for date management
- **Season Phase Detection**: Automatically detects current season phase (Pre-Season, Regular Season, Playoffs, etc.)
- **Week Number Calculation**: Calculates accurate week numbers for different season phases
- **Flexible Output**: Display standings by conference or league-wide
- **PEP-8 Compliant**: Clean, well-documented code following Python best practices

## Files

- `wnba_standings.py` - Main script for fetching and displaying standings
- `wnba_scores.py` - Script for fetching and displaying today's WNBA scores
- `wnba_dates.py` - Modular date management for WNBA 2025 season

## 2025 Season Schedule

- **Pre-season**: May 2 - May 15, 2025
- **Regular Season**: May 16 - September 11, 2025
- **Commissioner's Cup**: June 1 - June 17, 2025
- **All-Star Break**: July 17 - July 21, 2025
- **All-Star Game**: July 19, 2025
- **Playoffs**: September 14 - October 19, 2025

## Usage

### WNBA Standings

#### Show Season Schedule
```bash
python3 wnba_standings.py --show-dates
```

#### Display Standings by Conference (default)
```bash
python3 wnba_standings.py
```

#### Display Standings League-Wide
```bash
python3 wnba_standings.py --group league
```

### WNBA Scores

#### Show Today's Scores (default)
```bash
python3 wnba_scores.py
```

#### Show Scores for a Specific Date
```bash
python3 wnba_scores.py --date 2025-07-08
```

#### Show Scores with Different Timezone
```bash
python3 wnba_scores.py --timezone America/New_York
```

#### Show Season Schedule
```bash
python3 wnba_scores.py --show-dates
```

#### Debug API Response
```bash
python3 wnba_scores.py --debug
```

**Game Status Codes:**
- `F` - Final
- `F/OT` - Final (1st Overtime)
- `F/2OT` - Final (2nd Overtime)
- `F/3OT` - Final (3rd Overtime)
- `F/4OT` - Final (4th Overtime)
- `F/5OT` - Final (5th Overtime) and so on...
- `H` - Halftime
- `Q1`, `Q2`, `Q3`, `Q4` - Quarter 1, 2, 3, or 4
- `OT` - 1st Overtime (in progress)
- `2OT` - 2nd Overtime (in progress)
- `3OT` - 3rd Overtime (in progress)
- `Live` - Game in progress
- `Scheduled` - Game not yet started

### Show Help
```bash
python3 wnba_standings.py --help
python3 wnba_scores.py --help
```

## Requirements

- Python 3.6+
- `requests` library
- `pytz` library (for timezone support)

## Installation

```bash
pip install requests pytz
```

## API Server

The project includes a Flask/FastAPI server that provides both human-readable endpoints and JSON API endpoints.

### Starting the API Server

```bash
python3 wnba_api.py
```

This starts two servers:
- **Flask Server** (Port 5001): Human-readable curl-style endpoints
- **FastAPI Server** (Port 8001): JSON API endpoints with OpenAPI documentation

### Flask Endpoints (Human-Readable)

#### Help
```bash
curl http://localhost:5001/curl/help
```

#### Standings
```bash
# Conference standings (default)
curl http://localhost:5001/curl/standings

# League-wide standings
curl "http://localhost:5001/curl/standings?group=league"
```

#### Scores
```bash
# Today's scores
curl http://localhost:5001/curl/scores

# Scores for specific date
curl "http://localhost:5001/curl/scores?date=2025-07-08"

# Scores with timezone
curl "http://localhost:5001/curl/scores?timezone=America/New_York"
```

#### Schedule
```bash
# Today's schedule
curl http://localhost:5001/curl/schedule

# Schedule for specific date
curl "http://localhost:5001/curl/schedule?date=2025-07-08"

# Schedule with timezone
curl "http://localhost:5001/curl/schedule?timezone=America/New_York"
```

### FastAPI Endpoints (JSON)

#### Standings
```bash
curl http://localhost:8001/api/standings
```

#### Scores
```bash
curl http://localhost:8001/api/scores
curl "http://localhost:8001/api/scores?target_date=2025-07-08"
```

#### Schedule
```bash
curl http://localhost:8001/api/schedule
curl "http://localhost:8001/api/schedule?target_date=2025-07-08"
```

#### OpenAPI Documentation
Visit `http://localhost:8001/docs` in your browser for interactive API documentation.

### API Dependencies

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your RapidAPI key to `.env`:**
   ```
   WNBA_API_KEY=your_actual_api_key_here
   ```

3. **Get a RapidAPI key:**
   - Sign up at [RapidAPI](https://rapidapi.com)
   - Subscribe to the WNBA API
   - Copy your API key to the `.env` file

**Important:** Never commit your `.env` file to version control. It's already in `.gitignore`.

### Security Note

If you previously committed an API key to this repository, you can use the provided cleanup script to remove it from Git history:

```bash
./cleanup_git_history.sh
```

**⚠️ Warning:** This will rewrite Git history. Make sure to coordinate with collaborators if this is a shared repository.

## Scripts API

The individual scripts use the WNBA API via RapidAPI. You may need to update the API key in the scripts if it expires.

## Improvements Made

1. **Fixed Date Issues**: Updated from 2024 to 2025 season dates
2. **Modular Architecture**: Separated date logic into reusable module
3. **Better Error Handling**: Added timeout and improved error messages
4. **Type Hints**: Added proper type annotations for better code clarity
5. **PEP-8 Compliance**: Improved code formatting and documentation
6. **Season Phase Detection**: Accurate detection of current season phase
7. **Week Calculation**: Proper week number calculation for different phases
8. **Scores Script**: Added new script for fetching and displaying WNBA scores
9. **Timezone Support**: Added timezone support for scores display
10. **Flexible Date Input**: Can fetch scores for any date during the season
11. **Game Status Display**: Shows concise game status codes (F, Q1-Q4, H, Live, etc.)
12. **Debug Mode**: Added debug option to inspect API response structure
