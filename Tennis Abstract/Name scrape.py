import requests
import csv
import re
from bs4 import BeautifulSoup

def get_page_source(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching the page source:", e)
        return None

def add_space_before_uppercase(name):
    return re.sub(r'(?<=.)([A-Z])', r' \1', name)

# Fetch the webpage
page_source = get_page_source('http://tennisabstract.com/charting/meta.html')
if page_source is None:
    print("Failed to get the webpage")
    exit()

# Parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Assuming names are in <a> tags and href attributes contain the string "p="
names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

# Open a CSV file to store the names
with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()

    # Extract names, add spaces before uppercase letters, and write to the CSV
    for link in names_links:
        url = link.get('href')
        name = url.split("p=")[1]
        formatted_name = add_space_before_uppercase(name)
        writer.writerow({'name': formatted_name})

print("Scraping done. Names stored in names.csv.")
