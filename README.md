# Evaluating Tennis Styles

A Flask web application that analyzes and visualizes tennis player statistics by scraping data from Tennis Abstract. The application provides insights into player playing styles through rally length analysis, shot frequency, winner types, and unforced error patterns.

## Features


- **Statistical Analysis**: Breakdown of player statistics including:
  - Points by rally length (1-3, 4-6, 7-9, 10+ shots)
  - Shot frequency distribution
  - Winner types (Ace, Forehand, Backhand, Net)
  - Unforced error distribution
- **Comparative Analysis**: Compare player's recent performance against tour averages of the top 100
- **Keyword Generation**: Automatically identifies key characteristics of player's style

## Project Structure

### Core Application Files

#### `app.py`
The main Flask application file that handles web routes and server logic.

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

#### `requirements.txt`
Python dependencies for the application:
- `Flask` - Web framework
- `gunicorn` - Production WSGI server
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing library


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

## Data Sources

This project scrapes statistical data from Tennis Abstract's charting project. The charting data provides detailed shot-by-shot analysis of professional tennis matches.

- Player URLs follow the format: `https://www.tennisabstract.com/charting/{PlayerName}.html`
- Data includes tour-level matches with comprehensive shot tracking
- Statistics are divided into historical data (tour average) and recent performance (player's latest matches)

## Acknowledgments

All tennis statistics and data used in this application are sourced from **Tennis Abstract** (https://www.tennisabstract.com/), a comprehensive tennis statistics website created and maintained by **Jeff Sackmann**.

For more tennis data and analysis, please visit:
- Tennis Abstract: https://www.tennisabstract.com/
- Jeff Sackmann's GitHub: https://github.com/JeffSackmann
