import requests
import csv
import re
from bs4 import BeautifulSoup
import time
import random
import os

def get_page_source(url, retries=3, delay_min=1, delay_max=3):
    try:
        for attempt in range(retries):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            print(f"Failed to retrieve, status code: {response.status_code}. Retrying... (Attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(random.uniform(delay_min, delay_max))
        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching the page source:", e)
        return None

def add_space_before_uppercase(name):
    return re.sub(r'(?<=.)([A-Z])', r' \1', name)

def atp_top_100_scraper():
    # Fetch the webpage
    page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')
    if page_source is None:
        print("Failed to get the webpage")
        return

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Assuming names are in <a> tags and href attributes contain the string "p="
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Get the parent directory (project root) to save names.csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path_2 = os.path.join(parent_dir, 'atp_top_100.csv')

    # Open a CSV file to store the names
    with open(csv_path_2, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Extract names, add spaces before uppercase letters, and write to the CSV
        count = 0
        for link in names_links:
            if count >= 100:
                break
            url = link.get('href')
            if url and "p=" in url:
                try:
                    name = url.split("p=")[1]
                    formatted_name = add_space_before_uppercase(name)
                    writer.writerow({'name': formatted_name})
                    count += 1
                except IndexError:
                    print(f"Skipping malformed URL: {url}")
                    continue

    print(f"Scraping done. Names stored in {csv_path_2}")
############



def wta_top_100_scraper():
    # Fetch the webpage
    page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')
    if page_source is None:
        print("Failed to get the webpage")
        return

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Assuming names are in <a> tags and href attributes contain the string "p="
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Get the parent directory (project root) to save names.csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path_3 = os.path.join(parent_dir, 'wta_top_100.csv')

    # Open a CSV file to store the names
    with open(csv_path_3, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Extract names, add spaces before uppercase letters, and write to the CSV
        # Track when we find "woman" to start scraping after the second instance
        woman_count = 0
        scraping_started = False
        count = 0

        for link in names_links:
            if count >= 100:
                break
            url = link.get('href')
            if url and "p=" and "wplayer" in url:
                try:
                    name = url.split("p=")[1]
                    formatted_name = add_space_before_uppercase(name)
                    writer.writerow({'name': formatted_name})
                    count += 1
                except IndexError:
                    print(f"Skipping malformed URL: {url}")
                    continue

    print(f"Scraping done. Names stored in {csv_path_3}")

def all_atp_players_scraper():
    """
    Scrapes ALL ATP players from Tennis Abstract and saves to CSV.
    """
    # Fetch the webpage
    page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')
    if page_source is None:
        print("Failed to get the webpage")
        return

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Assuming names are in <a> tags and href attributes contain the string "p="
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Get the parent directory (project root) to save CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path = os.path.join(parent_dir, 'all_atp_players.csv')

    # Open a CSV file to store the names
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Extract names, add spaces before uppercase letters, and write to the CSV
        # Only get ATP players (those WITHOUT "wplayer" in the URL)
        count = 0
        for link in names_links:
            url = link.get('href')
            if url and "p=" in url and "wplayer" not in url:
                try:
                    name = url.split("p=")[1]
                    formatted_name = add_space_before_uppercase(name)
                    writer.writerow({'name': formatted_name})
                    count += 1
                except IndexError:
                    print(f"Skipping malformed URL: {url}")
                    continue

    print(f"ATP scraping done. {count} players stored in {csv_path}")

def all_wta_players_scraper():
    """
    Scrapes ALL WTA players from Tennis Abstract and saves to CSV.
    """
    # Fetch the webpage
    page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')
    if page_source is None:
        print("Failed to get the webpage")
        return

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Assuming names are in <a> tags and href attributes contain the string "p="
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Get the parent directory (project root) to save CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path = os.path.join(parent_dir, 'all_wta_players.csv')

    # Open a CSV file to store the names
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Extract names, add spaces before uppercase letters, and write to the CSV
        # Only get WTA players (those WITH "wplayer" in the URL)
        count = 0
        for link in names_links:
            url = link.get('href')
            if url and "p=" in url and "wplayer" in url:
                try:
                    name = url.split("p=")[1]
                    formatted_name = add_space_before_uppercase(name)
                    writer.writerow({'name': formatted_name})
                    count += 1
                except IndexError:
                    print(f"Skipping malformed URL: {url}")
                    continue

    print(f"WTA scraping done. {count} players stored in {csv_path}")



all_wta_players_scraper()