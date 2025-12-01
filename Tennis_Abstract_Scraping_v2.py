import requests
import re
import csv
import time
import random
import os
from bs4 import BeautifulSoup


# Load formatted data from CSV files
def load_formatted_data_from_csv():
    """
    Loads the formatted data from CSV files into global variables.
    Returns them in the format: [['Header', 'Count', 'Percentage'], ['Type', count, 'X.XX%'], ...]
    """
    def load_csv(filename):
        """Helper function to load a single CSV file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.exists(filepath):
            # Return default empty data if file doesn't exist
            return [['Type', 'Count', 'Percentage']]

        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for i, row in enumerate(reader):
                if i == 0:
                    # Header row - keep as strings
                    data.append(row)
                else:
                    # Data rows - convert count to int, keep percentage as string
                    data.append([row[0], int(row[1]), row[2]])
            return data

    atp_winners = load_csv('atp_winners_formatted.csv')
    atp_errors = load_csv('atp_errors_formatted.csv')
    wta_winners = load_csv('wta_winners_formatted.csv')
    wta_errors = load_csv('wta_errors_formatted.csv')

    return atp_winners, atp_errors, wta_winners, wta_errors

# Load the data into global variables
atp_winners_formatted, atp_errors_formatted, wta_winners_formatted, wta_errors_formatted = load_formatted_data_from_csv()


def get_page_source(url, retries=3, delay_min=1, delay_max=3):
    try:
        for _ in range(retries):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            print(f"Failed to retrieve, status code: {response.status_code}. Retrying...")
            time.sleep(random.uniform(delay_min, delay_max))
        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching the page source:", e)
        return None



def display_table(table):
    # Update to support dynamic columns
    column_widths = [max(len(str(row[col_idx])) for row in table) for col_idx in range(len(table[0]))]
    header_divider = "+".join(["-" * (width + 2) for width in column_widths])
    print(header_divider)
    for row in table:
        print("| " + " | ".join(str(cell).ljust(width) for cell, width in zip(row, column_widths)) + " |")
        print(header_divider)


def fetch_tennis_data(url, display = True):
    page_source = get_page_source(url)

    if page_source is None:
        exit("Failed to retrieve the page source.")

    pattern = re.compile(r"'(Ace|Forehand|Backhand|Net)', (\d+)]")
    matches = pattern.findall(page_source)
    header = ["Winner Type", "Count", "Percentage"]

    # Create data_rows and calculate total counts for olddata and newdata
    data_rows = [[winner_type, int(count)] for winner_type, count in matches]
    half_index = len(data_rows) // 4
    total_count_old = sum(count for _, count in data_rows[:half_index])
    total_count_new = sum(count for _, count in data_rows[half_index:half_index + 4])

    # Extract player name from the URL
    # URL format: http://www.tennisabstract.com/charting/PlayerName.html
    player_name = url.split('/')[-1].replace('.html', '')

    # Fetch the meta page to check if player is WTA or ATP
    meta_page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')

    # Parse the HTML content
    soup = BeautifulSoup(meta_page_source, 'html.parser')

    # Find all links with "p=" in href
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Search for the player name in the links and check if it contains "wplayer"
    is_wta_player = False
    for link in names_links:
        link_href = link.get('href')
        if link_href and "p=" in link_href:
            # Extract the name from the href (format: ?p=PlayerName)
            link_player_name = link_href.split('p=')[1] if 'p=' in link_href else ''
            # Check if this is our player
            if link_player_name.lower() == player_name.lower():
                # Check if this link contains "wplayer"
                if "wplayer" in link_href:
                    is_wta_player = True
                break

    # Create olddata and newdata with percentages
    # Set olddata based on player gender
    if is_wta_player:
        olddata = wta_winners_formatted
    else:
        olddata = atp_winners_formatted
    newdata = [header] + [[winner_type, count, "{:.2f}%".format((count / total_count_new) * 100)] for winner_type, count in data_rows[half_index:half_index + 4]]
    title = header[0]

    if display:
        print("Old Data:")
        display_table(olddata)
        print("\nNew Data:")
        display_table(newdata)
    return olddata, newdata

# Example usage
url = "http://www.tennisabstract.com/charting/NovakDjokovic.html"
#fetch_tennis_data(url)

#fetch_tennis_data function stitches together the old and newdata

#Shot length
def fetch_tennis_data_2(url, display = True):
    page_source = get_page_source(url)

    # Check if the page source was successfully fetched
    if page_source is None:
        exit("Failed to retrieve the page source.")

    # Regular expression pattern to extract numbers after 'Points by Rally Length' values
    pattern = re.compile(r"'(1 to 3 shots|4 to 6 shots|7 to 9 shots|10\+ shots)', (\d+)]")

    # Find all matches
    matches = pattern.findall(page_source)

    # Create a table format
    header = ["Points by Rally Length", "Count", "Percentage"]

    # Create data_rows and calculate total counts for olddata and newdata
    data_rows = [[rally_type, int(count)] for rally_type, count in matches]
    half_index = len(data_rows) // 2
    total_count_old = sum(count for _, count in data_rows[:half_index])
    total_count_new = sum(count for _, count in data_rows[half_index:half_index + 4])

    # Create olddata and newdata with percentages
    olddata = [header] + [[rally_type, count, "{:.2f}%".format((count / total_count_old) * 100)] for rally_type, count in data_rows[:half_index]]
    newdata = [header] + [[rally_type, count, "{:.2f}%".format((count / total_count_new) * 100)] for rally_type, count in data_rows[half_index:half_index + 4]]
    title = header[0]

    if display:
        print("Old Data:")
        display_table(olddata)
        print("\nNew Data:")
        display_table(newdata)
    return olddata, newdata

# Example Usage:
url = "http://www.tennisabstract.com/charting/NovakDjokovic.html"
#fetch_tennis_data_2(url)




#Shot Frequency
def fetch_tennis_data_3(url, display = True):
    page_source = get_page_source(url)

    # Check if the page source was successfully fetched
    if page_source is None:
        exit("Failed to retrieve the page source.")

    # Regular expression pattern to extract numbers after 'Shot Frequency' values
    pattern = re.compile(r"'(FH Drive|BH Drive|FH Slice|BH Slice|Dropshot|Lob|Net)', (\d+)]")

    # Find all matches
    matches = pattern.findall(page_source)

    # Create a table format
    header = ["Shot Frequency", "Count", "Percentage"]

    # Create data_rows and calculate total counts for olddata and newdata
    data_rows = [[shot_type, int(count)] for shot_type, count in matches]
    
    # Here we determine the indices for old and new data; modify as needed
    old_indices = slice(4, 11)
    new_indices = slice(11, len(data_rows))

    total_count_old = sum(count for _, count in data_rows[old_indices])
    total_count_new = sum(count for _, count in data_rows[new_indices])

    # Create olddata and newdata with percentages
    olddata = [header] + [[shot_type, count, "{:.2f}%".format((count / total_count_old) * 100)] for shot_type, count in data_rows[old_indices]]
    newdata = [header] + [[shot_type, count, "{:.2f}%".format((count / total_count_new) * 100)] for shot_type, count in data_rows[new_indices]]
    title = header[0]

    if display:
        print("Old Data:")
        display_table(olddata)
        print("\nNew Data:")
        display_table(newdata)
    return olddata, newdata

# Example Usage:
url = "http://www.tennisabstract.com/charting/IgaSwiatek.html"
#fetch_tennis_data_3(url)

#Unforced errors
def fetch_tennis_data_4(url, display = True):
    page_source = get_page_source(url)

    # Check if the page source was successfully fetched
    if page_source is None:
        exit("Failed to retrieve the page source.")

    # Regular expression pattern to extract numbers after 'Unforced Error' values
    pattern = re.compile(r"'(Double Fault|Forehand|Backhand|Net)', (\d+)]")

    # Find all matches
    matches = pattern.findall(page_source)

    # Create a table format
    header = ["Unforced Error", "Count", "Percentage"]

    # Create data_rows and calculate total counts for olddata and newdata
    data_rows = [[error_type, int(count)] for error_type, count in matches]
    
    # Here we determine the indices for old and new data; modify as needed
    old_indices = slice(6, 10)
    new_indices = slice(10, 14)

    total_count_old = sum(count for _, count in data_rows[old_indices])
    total_count_new = sum(count for _, count in data_rows[new_indices])

    # Create olddata and newdata with percentages
    # Extract player name from the URL
    # URL format: http://www.tennisabstract.com/charting/PlayerName.html
    player_name = url.split('/')[-1].replace('.html', '')

    # Fetch the meta page to check if player is WTA or ATP
    meta_page_source = get_page_source('https://www.tennisabstract.com/charting/meta.html')

    # Parse the HTML content
    soup = BeautifulSoup(meta_page_source, 'html.parser')

    # Find all links with "p=" in href
    names_links = soup.find_all('a', href=lambda href: (href and "p=" in href))

    # Search for the player name in the links and check if it contains "wplayer"
    is_wta_player = False
    for link in names_links:
        link_href = link.get('href')
        if link_href and "p=" in link_href:
            # Extract the name from the href (format: ?p=PlayerName)
            link_player_name = link_href.split('p=')[1] if 'p=' in link_href else ''
            # Check if this is our player
            if link_player_name.lower() == player_name.lower():
                # Check if this link contains "wplayer"
                if "wplayer" in link_href:
                    is_wta_player = True
                break

    # Set olddata based on player gender
    if is_wta_player:
        olddata = wta_errors_formatted
    else:
        olddata = atp_errors_formatted

    newdata = [header] + [[error_type, count, "{:.2f}%".format((count / total_count_new) * 100)] for error_type, count in data_rows[new_indices]]
    title = header[0]

    if display:
        print("Old Data:")
        display_table(olddata)
        print("\nNew Data:")
        display_table(newdata)
    return olddata, newdata

# Example Usage:
url = "http://www.tennisabstract.com/charting/NovakDjokovic.html"
#fetch_tennis_data_4(url)



'''
# Your display_percentage_difference_2 function (unchanged)
def display_percentage_difference(olddata, newdata, title):
    header = [title, "Percentage Difference"]
    percentage_difference_data = [header]
    for old_row, new_row in zip(olddata[1:], newdata[1:]):
        old_percentage = float(old_row[-1][:-1])
        new_percentage = float(new_row[-1][:-1])
        difference = new_percentage - old_percentage
        percentage_difference_data.append([old_row[0], "{:.2f}%".format(difference)])
    print("\nPercentage Difference:")
    display_table(percentage_difference_data)
'''

def display_percentage_difference(olddata, newdata, title):
    # Initialize the header and result list
    header = [title, "Percentage"]
    percentage_difference_data = [header]
    
    for old_row, new_row in zip(olddata[1:], newdata[1:]):
        # Extract the old and new percentages and convert them to floats
        old_percentage = float(old_row[-1][:-1])
        new_percentage = float(new_row[-1][:-1])
        
        # Calculate the percentage difference
        difference = new_percentage - old_percentage
        
        # Append to result list
        percentage_difference_data.append([old_row[0], "{:.2f}%".format(difference)])

    return percentage_difference_data

# Example Usage
url = "http://www.tennisabstract.com/charting/NovakDjokovic.html"



olddata_2, newdata_2 = fetch_tennis_data_2(url, display=False)
#display_percentage_difference(olddata_2, newdata_2, "Points by Rally Length")

olddata_3, newdata_3 = fetch_tennis_data_3(url, display=False)
#display_percentage_difference(olddata_3, newdata_3, "Shot Frequency")

olddata, newdata = fetch_tennis_data(url, display=False)
#display_percentage_difference(olddata, newdata, "Winner Type")

olddata_4, newdata_4 = fetch_tennis_data_4(url, display=False)
#display_percentage_difference(olddata_4, newdata_4, "Unforced Error")


def fetch_all_tennis_data(url):

    print("Fetching points by rally length data...")
    fetch_tennis_data_2(url)
    print("\nFetching shot frequency data...")
    fetch_tennis_data_3(url)
    print("\nFetching winner types data...")
    fetch_tennis_data(url)
    print("\nFetching unforced errors data...")
    fetch_tennis_data_4(url)

    

# Example usage
url = "http://www.tennisabstract.com/charting/NovakDjokovic.html"
#fetch_all_tennis_data(url)



def fetch_all_percentage_data(url):
    olddata_2, newdata_2 = fetch_tennis_data_2(url, display=False)
    percentdata_2 = display_percentage_difference(olddata_2, newdata_2, "Points by Rally Length")

    olddata_3, newdata_3 = fetch_tennis_data_3(url, display=False)
    percentdata_3 = display_percentage_difference(olddata_3, newdata_3, "Shot Frequency")

    olddata, newdata = fetch_tennis_data(url, display=False)
    percentdata = display_percentage_difference(olddata, newdata, "Winner Type")

    olddata_4, newdata_4 = fetch_tennis_data_4(url, display=False)
    percentdata_4 = display_percentage_difference(olddata_4, newdata_4, "Unforced Error")

    return percentdata_2, percentdata_3, percentdata, percentdata_4

fetch_all_percentage_data(url)

percentdata_2, percentdata_3, percentdata, percentdata_4 = fetch_all_percentage_data(url)


#percentdata_2 = display_percentage_difference(olddata_2, newdata_2, "Points by Rally Length")

#percentdata_3 = display_percentage_difference(olddata_3, newdata_3, "Shot Frequency")

#percentdata = display_percentage_difference(olddata, newdata, "Winner Type")

#percentdata_4 = display_percentage_difference(olddata_4, newdata_4, "Unforced Error")

#print(olddata_2)



def fetch_matches(url, display = False):
    page_source = get_page_source(url)

    if page_source is None:
        exit("Failed to retrieve the page source.")

    # Updated regular expression pattern to find the word 'matches' and the word before it (presumably a number)
    pattern = re.compile(r'(\d+)\s+matches')
    match = pattern.search(page_source)

    nummatches = None
    if match:
        # If the pattern is found, capture the word prior to "matches" into the variable nummatches
        nummatches = match.group(1)

    if display and nummatches:
        print(f"Number of matches: {nummatches}")
        
    return nummatches

#fetch_matches(url)


all_percentage_data = [percentdata_2, percentdata_3, percentdata, percentdata_4]

def find_keywords(all_percentage_data):
    keyword_list = []
    tenacious1_met = False
    tenacious2_met = False
    aggressive1_met = False
    aggressive2_met = False
    forehand_drive_met = False
    backhand_drive_met = False
    net_met = False
    strong_forehand_met = False
    strong_backhand_met = False
    big_serve_met = False
    variety_counter = 0
    for table in all_percentage_data:
        for row in table[1:]:  # Skip the header row
            label = row[0]
            percentage = row[1]

            # Strip the '%' symbol and convert to float
            try:
                percentage_value = float(percentage.strip('%'))
            except ValueError:
                continue

            # Check the condition for '1 to 3 shots'
            if label == '1 to 3 shots' and percentage_value > 0:
                aggressive1_met = True

            if label == '4 to 6 shots' and percentage_value > 0:
                aggressive2_met = True

            # Check the first condition
            if label == '7 to 9 shots' and percentage_value > 0:
                tenacious1_met = True

            # Check the second condition
            if label == '10+ shots' and percentage_value > 0:
                tenacious2_met = True

            if label == 'FH Drive' and percentage_value > 0:
                forehand_drive_met = True

            if label == 'BH Drive' and percentage_value > 0:
                backhand_drive_met = True

            if label == 'FH slice' and percentage_value > 0:
                variety_counter +=1

            if label == 'BH Slice' and percentage_value > 0:
                variety_counter +=1

            if label == 'Dropshot' and percentage_value > 0:
                variety_counter +=1

            if label == 'Lob' and percentage_value > 0:
                variety_counter +=1

            if label == 'Net' and percentage_value > 0:
                net_met = True

            if label == 'Ace' and percentage_value > 0:
                big_serve_met = True

    if tenacious1_met and tenacious2_met and aggressive1_met:
        if float((all_percentage_data[0][3][1].rstrip('%')) or float(all_percentage_data[0][4][1].rstrip('%')))> float(all_percentage_data[0][1][1].rstrip('%')):
            keyword_list.append("Grinder")
        else:
            keyword_list.append("First-Strike")

    if aggressive1_met and tenacious1_met == False and tenacious2_met == False:
        keyword_list.append('First-Strike')
    
    if tenacious1_met and tenacious2_met and aggressive1_met == False:
        keyword_list.append('Grinder')
    
    if tenacious1_met and tenacious2_met == False and aggressive1_met and aggressive2_met:
        keyword_list.append('First-Strike') 

    if forehand_drive_met and backhand_drive_met == False:
        keyword_list.append('Likes to hit forehands')

    if forehand_drive_met == False and backhand_drive_met:
        keyword_list.append('Likes to hit backhands')

    if forehand_drive_met and backhand_drive_met:
        if float(all_percentage_data[1][1][1].rstrip('%')) > 1 + float(all_percentage_data[1][2][1].rstrip('%')):
            keyword_list.append('Likes to hit groundstrokes (mainly Forehand)')
        elif float(all_percentage_data[1][2][1].rstrip('%')) > 1 + float(all_percentage_data[1][1][1].rstrip('%')):
            keyword_list.append('Likes to hit groundstrokes (mainly Backhand)')
        else:
            keyword_list.append('Likes to hit groundstrokes')

    if variety_counter >= 2:
        keyword_list.append('Uses variety')

    if net_met:
        keyword_list.append('Likes to go to net')
        
    if float(all_percentage_data[2][2][1].rstrip('%')) > 0:
        strong_forehand_met = True
    
    if float(all_percentage_data[2][3][1].rstrip('%')) > 0:
        strong_backhand_met = True

    if strong_forehand_met and strong_backhand_met == False:
        keyword_list.append("Strong Forehand")

    if strong_forehand_met == False and strong_backhand_met:
        keyword_list.append("Strong Backhand")

    if strong_forehand_met and strong_backhand_met:
        if float(all_percentage_data[2][2][1].rstrip('%')) > 1 + float(all_percentage_data[2][3][1].rstrip('%')):
            keyword_list.append("Aggressive Baseliner with Strong Forehand")
        elif float(all_percentage_data[2][3][1].rstrip('%')) > 1 + float(all_percentage_data[2][2][1].rstrip('%')):
            keyword_list.append("Aggressive Baseliner with Strong Backhand")
        else:
            keyword_list.append('Aggressive Baseliner')

    if big_serve_met:
        keyword_list.append("Big Serve")
        


    return keyword_list

# Find keywords based on the fetched data
keywords = find_keywords(all_percentage_data)

#print(keywords)
#print(fetch_tennis_data("http://www.tennisabstract.com/charting/NovakDjokovic.html"))