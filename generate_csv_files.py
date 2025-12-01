"""
Script to generate CSV files needed for deployment.
This should be run during the build process on Render.
"""
import os

# Ensure csv_files directory exists
csv_dir = 'csv_files'
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
    print(f"Created {csv_dir} directory")

# Try to import and run the scraper functions
try:
    from Name_scrape_top_100 import all_atp_players_scraper, all_wta_players_scraper, atp_top_100_scraper, wta_top_100_scraper

    print("Scraping ATP players...")
    all_atp_players_scraper()

    print("Scraping WTA players...")
    all_wta_players_scraper()

    print("Scraping top 100 ATP...")
    atp_top_100_scraper()

    print("Scraping top 100 WTA...")
    wta_top_100_scraper()

    print("All CSV files generated successfully!")
except Exception as e:
    print(f"Error generating CSV files: {e}")
    print("Creating minimal CSV files as fallback...")

    # Create minimal CSV files as fallback
    import csv

    minimal_players = [
        ['name'],
        ['Novak Djokovic'],
        ['Carlos Alcaraz'],
        ['Jannik Sinner'],
        ['Iga Swiatek'],
        ['Aryna Sabalenka'],
        ['Coco Gauff']
    ]

    for filename in ['all_atp_players.csv', 'all_wta_players.csv', 'atp_top_100.csv', 'wta_top_100.csv']:
        filepath = os.path.join(csv_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(minimal_players)
        print(f"Created fallback {filename}")
