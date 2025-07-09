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
- `wnba_dates.py` - Modular date management for WNBA 2025 season

## 2025 Season Schedule

- **Pre-season**: May 2 - May 15, 2025
- **Regular Season**: May 16 - September 11, 2025
- **Commissioner's Cup**: June 1 - June 17, 2025
- **All-Star Break**: July 17 - July 21, 2025
- **All-Star Game**: July 19, 2025
- **Playoffs**: September 14 - October 19, 2025

## Usage

### Show Season Schedule
```bash
python3 wnba_standings.py --show-dates
```

### Display Standings by Conference (default)
```bash
python3 wnba_standings.py
```

### Display Standings League-Wide
```bash
python3 wnba_standings.py --group league
```

### Show Help
```bash
python3 wnba_standings.py --help
```

## Requirements

- Python 3.6+
- `requests` library

## Installation

```bash
pip install requests
```

## API

The script uses the WNBA API via RapidAPI. You may need to update the API key in the script if it expires.

## Improvements Made

1. **Fixed Date Issues**: Updated from 2024 to 2025 season dates
2. **Modular Architecture**: Separated date logic into reusable module
3. **Better Error Handling**: Added timeout and improved error messages
4. **Type Hints**: Added proper type annotations for better code clarity
5. **PEP-8 Compliance**: Improved code formatting and documentation
6. **Season Phase Detection**: Accurate detection of current season phase
7. **Week Calculation**: Proper week number calculation for different phases
