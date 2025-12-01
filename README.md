# Evaluating Tennis Styles

A Flask web application that analyzes and visualizes tennis player statistics by scraping data from Tennis Abstract. The application provides insights into player playing styles through rally length analysis, shot frequency, winner types, and unforced error patterns.

## Features

- **Player Search**: Autocomplete search functionality for ATP and WTA players
- **Statistical Analysis**: Comprehensive breakdown of player statistics including:
  - Points by rally length (1-3, 4-6, 7-9, 10+ shots)
  - Shot frequency distribution
  - Winner types (Ace, Forehand, Backhand, Net)
  - Unforced error patterns
- **Comparative Analysis**: Compare player's recent performance against tour averages
- **Keyword Generation**: Automatically identifies key characteristics of player's style
- **24-Hour Caching**: Improved performance with file-based caching system
- **Anti-Blocking Features**: Sophisticated request handling to avoid server blocks

## Project Structure

### Core Application Files

#### `app.py`
The main Flask application file that handles web routes and server logic.
- **Routes**:
  - `/` - Home page with player search interface
  - `/search` - AJAX endpoint for player name autocomplete
  - `/tennis_data/<name>` - Displays detailed statistics for a specific player
- **Functionality**:
  - Loads player names from CSV files in the `csv_files/` directory
  - Implements caching system to reduce server load
  - Handles errors gracefully with custom error pages

#### `Tennis_Abstract_Scraping_v2.py`
The core scraping and data processing module.
- **Key Functions**:
  - `get_page_source()` - Fetches HTML with browser-like headers and session management
  - `fetch_tennis_data()` - Scrapes winner type data (Ace, Forehand, Backhand, Net)
  - `fetch_tennis_data_2()` - Scrapes points by rally length data
  - `fetch_tennis_data_3()` - Scrapes shot frequency data
  - `fetch_tennis_data_4()` - Scrapes unforced error data
  - `display_percentage_difference()` - Calculates percentage differences between player and tour average
  - `fetch_matches()` - Gets the number of matches analyzed
  - `find_keywords()` - Generates descriptive keywords based on statistical patterns
- **Caching Functions**:
  - `get_cached_data()` - Retrieves cached player data if fresh (< 24 hours)
  - `save_to_cache()` - Saves fetched data to JSON cache files
  - `is_cache_fresh()` - Checks if cached data is still valid
- **Features**:
  - Session-based HTTP requests for connection pooling
  - Comprehensive browser headers to avoid detection
  - Smart retry logic with exponential backoff
  - WTA player detection using CSV lookup
  - Formatted data loading from CSV files

### Data Collection Files

#### `Name_scrape_top_100.py`
Scrapes player names from Tennis Abstract's meta page.
- **Functions**:
  - `get_page_source()` - Fetches webpage with retry logic
  - `add_space_before_uppercase()` - Formats player names (e.g., "NovakDjokovic" → "Novak Djokovic")
  - `atp_top_100_scraper()` - Scrapes top 100 ATP players
  - `wta_top_100_scraper()` - Scrapes top 100 WTA players (filters for "wplayer" in URLs)
  - `all_atp_players_scraper()` - Scrapes all ATP players with charting data
  - `all_wta_players_scraper()` - Scrapes all WTA players with charting data
- **Output**: CSV files saved to `csv_files/` directory

#### `generate_csv_files.py`
Build script that generates player name CSV files during deployment.
- **Purpose**: Runs during Render deployment to populate player database
- **Process**:
  1. Creates `csv_files/` directory if it doesn't exist
  2. Calls scraper functions with 2-second delays between operations
  3. Falls back to minimal player list if scraping fails
- **Fallback Players**: Novak Djokovic, Carlos Alcaraz, Jannik Sinner, Iga Swiatek, Aryna Sabalenka, Coco Gauff

#### `Testing.py` (Development)
Development file for testing data formatting functions.
- Contains `format_winners_data()` and `format_errors_data()` functions
- Used to generate formatted CSV files for tour averages

#### `winners_and_unforced_from_top_100.py` (Development)
Script to scrape and compile statistics from top 100 players.
- Iterates through top player lists
- Fetches winner and unforced error data
- Aggregates statistics for tour average calculations

### Frontend Files

#### `templates/home.html`
Landing page with player search functionality.
- jQuery autocomplete for player search
- Responsive design
- Links to player statistics pages

#### `templates/tennis_data.html`
Player statistics display page.
- Side-by-side comparison of player stats vs tour average
- Color-coded percentage differences (red for negative, green for positive)
- Displays all four statistical categories
- Shows keywords describing player's style
- Links to original Tennis Abstract player page

#### `templates/error.html`
Custom error page for failed requests.
- Displays user-friendly error messages
- Handles cases where player data is unavailable or server blocks occur

### Configuration Files

#### `requirements.txt`
Python dependencies for the application:
- `Flask` - Web framework
- `gunicorn` - Production WSGI server
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing library

#### `build.sh`
Render deployment build script.
- Installs Python dependencies
- Runs `generate_csv_files.py` to populate player database

#### `.gitignore`
Specifies files to exclude from version control:
- `cache/` - Cached player data (regenerated as needed)
- `__pycache__/` - Python bytecode
- IDE and OS specific files

### Data Directories

#### `csv_files/`
Contains player name lists and tour average data:
- `all_atp_players.csv` - Complete list of ATP players
- `all_wta_players.csv` - Complete list of WTA players
- `atp_top_100.csv` - Top 100 ATP players
- `wta_top_100.csv` - Top 100 WTA players
- `names.csv` - Legacy player names file
- `atp_winners_formatted.csv` - ATP tour average for winner types
- `atp_errors_formatted.csv` - ATP tour average for unforced errors
- `wta_winners_formatted.csv` - WTA tour average for winner types
- `wta_errors_formatted.csv` - WTA tour average for unforced errors

#### `cache/`
Stores cached player data as JSON files (auto-generated):
- File naming: `{playername}.json` (e.g., `novakdjokovic.json`)
- Cache duration: 24 hours
- Structure: Contains all fetched data, percentages, keywords, and timestamp

### Legacy Directory

#### `Tennis Abstract/`
Contains older versions of scraping scripts for reference.

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/PSS128/Evaluating-Tennis-Styles.git
cd Evaluating-Tennis-Styles
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate player CSV files:
```bash
python generate_csv_files.py
```

4. Run the application:
```bash
python app.py
```

5. Open browser to `http://localhost:5000`

### Deployment on Render

1. Connect your GitHub repository to Render
2. Configure as a Web Service
3. Build command: `bash build.sh`
4. Start command: `gunicorn app:app`
5. Render will automatically run the build script and start the application

## How It Works

1. **Player Search**: User searches for a player using the autocomplete search bar
2. **Cache Check**: Application checks if player data exists in cache and is fresh (< 24 hours)
3. **Data Retrieval**:
   - If cached: Returns data instantly
   - If not cached: Scrapes Tennis Abstract with anti-blocking measures
4. **Data Processing**:
   - Fetches 4 different statistical categories
   - Loads appropriate tour average (ATP/WTA) from CSV files
   - Calculates percentage differences
   - Generates descriptive keywords
5. **Caching**: Saves fetched data to cache for 24 hours
6. **Display**: Renders statistics in side-by-side comparison format

## Anti-Blocking Features

To avoid being blocked by Tennis Abstract, the application implements:

- **Session Management**: Maintains cookies and connection pooling
- **Browser-Like Headers**: Comprehensive headers (User-Agent, Accept, DNT, Referer, etc.)
- **Smart Retry Logic**: 3 retries with random delays (1-3 seconds)
- **Special 403 Handling**: Longer delays (3-5 seconds) when encountering blocks
- **Random Delays**: Mimics human browsing patterns
- **24-Hour Caching**: Reduces total requests by ~95%
- **Build Delays**: 2-second delays between operations during deployment

## Technical Details

- **Language**: Python 3
- **Framework**: Flask
- **Web Server**: Gunicorn (production)
- **Scraping**: Requests + BeautifulSoup4
- **Caching**: File-based JSON storage
- **Hosting**: Render (or any Python hosting platform)

## Data Sources

This project scrapes statistical data from Tennis Abstract's charting project. The charting data provides detailed shot-by-shot analysis of professional tennis matches.

- Player URLs follow the format: `https://www.tennisabstract.com/charting/{PlayerName}.html`
- Data includes tour-level matches with comprehensive shot tracking
- Statistics are divided into historical data (tour average) and recent performance (player's latest matches)

## Acknowledgments

All tennis statistics and data used in this application are sourced from **Tennis Abstract** (https://www.tennisabstract.com/), a comprehensive tennis statistics website created and maintained by **Jeff Sackmann**.

Jeff Sackmann's Tennis Abstract project provides invaluable detailed match charting data and statistical analysis for professional tennis. This application would not be possible without his extensive work in collecting and publishing tennis statistics.

For more tennis data and analysis, please visit:
- Tennis Abstract: https://www.tennisabstract.com/
- Jeff Sackmann's GitHub: https://github.com/JeffSackmann
