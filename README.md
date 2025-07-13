# SportsPuff - Multi-Sport API Server

A Python API server that fetches and serves sports data for WNBA, NBA, NHL, MLB, and NFL with accurate date calculations, season phase detection, and dynamic season management.

## Features

- **Multi-Sport Support**: WNBA, NBA, NHL, MLB, and NFL data
- **Dynamic Season Management**: Automatic season detection and phase calculation
- **Dual API Interface**: Human-readable curl endpoints and JSON API endpoints
- **Season Analytics**: Progress tracking, milestone detection, and transition monitoring
- **Interactive Dashboard**: CLI interface for season management and analytics
- **Modular Design**: Separate modules for each sport and functionality
- **PEP-8 Compliant**: Clean, well-documented code following Python best practices

## Files

### Core API Server
- `wnba_api.py` - Main API server with Flask and FastAPI endpoints
- `sports_api.py` - Generic sports data fetching module
- `sports_config.py` - Sports configuration and season management
- `season_manager.py` - Dynamic season management and detection

### Season Management
- `manage_seasons.py` - Interactive season management utility
- `season_analytics.py` - Season progress and milestone analytics
- `season_transitions.py` - Season transition monitoring
- `season_predictor.py` - Future season prediction
- `season_dashboard.py` - Master CLI dashboard for all season tools
- `seasons.json` - Season data configuration file

### WNBA Modules
- `wnba_standings.py` - WNBA standings fetching
- `wnba_scores.py` - WNBA scores fetching
- `wnba_schedule.py` - WNBA schedule fetching
- `wnba_dates.py` - WNBA date management
- `wnba_config.py` - WNBA configuration

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

### Dependencies

#### Core Dependencies (Required)
For the main WNBA scripts (scores, standings, schedule):
```bash
pip install -r requirements.txt
```

#### API Server Dependencies (Optional)
If you want to run the API server (`wnba_api.py`):
```bash
pip install -r requirements-api.txt
```

**Note:** The API server dependencies include Flask, FastAPI, and Pydantic which may have compatibility issues with Python 3.13+. If you encounter installation errors, you can still use the core scripts without the API server.

### Environment Setup

1. **Create a `.env` file in the project root:**
   ```bash
   touch .env
   ```

2. **Add your API key to `.env`:**
   
   **For SportsBlaze API (recommended):**
   ```
   SPORTSBLAZE_API_KEY=your_actual_sportsblaze_api_key_here
   ```
   
   **For RapidAPI (legacy support):**
   ```
   WNBA_API_KEY=your_actual_rapidapi_key_here
   ```

3. **Get an API key:**
   
   **SportsBlaze API (recommended):**
   - Sign up at [SportsBlaze](https://sportsblaze.com)
   - Subscribe to the WNBA API
   - Copy your API key to the `.env` file as `SPORTSBLAZE_API_KEY`
   
   **RapidAPI (legacy):**
   - Sign up at [RapidAPI](https://rapidapi.com)
   - Subscribe to the WNBA API
   - Copy your API key to the `.env` file as `WNBA_API_KEY`

**Important:** Never commit your `.env` file to version control. It's already in `.gitignore`.

## Quick Setup and Testing

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script to create virtual environment and install dependencies
./setup_dev.sh

# Activate the virtual environment
source venv/bin/activate

# Test your setup
python3 test_setup.py
```

**If you encounter installation errors** (especially with pydantic-core on Python 3.13+):
```bash
# Run the fix script to resolve installation issues
./fix_installation.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test your setup
python3 test_setup.py
```

### Testing Your Setup
After setting up your virtual environment and adding your API key to `.env`, run:
```bash
python3 test_setup.py
```

This will verify:
- All required packages are installed
- Your `.env` file exists and contains an API key
- API configuration is working correctly
- All scripts can be imported successfully

### Security Note

If you previously committed an API key to this repository, you can use the provided cleanup script to remove it from Git history:

```bash
./cleanup_git_history.sh
```

**⚠️ Warning:** This will rewrite Git history. Make sure to coordinate with collaborators if this is a shared repository.

## Scripts API

The individual scripts use the WNBA API via SportsBlaze (recommended) or RapidAPI (legacy support). The scripts automatically detect which API to use based on your environment variables:

- If `SPORTSBLAZE_API_KEY` is set, it will use SportsBlaze API
- If `WNBA_API_KEY` is set, it will use RapidAPI (legacy)
- If neither is set, it will show an error message

You may need to update the API key in your `.env` file if it expires.

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
