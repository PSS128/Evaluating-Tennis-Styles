import sys
import os

#print(fetch_tennis_data_4(url, display=False))


### Take the ATP top 100, get the links
### Scrape the data for winners and unforced errors
### Replace the data into Tennis_Abstract_Scraping
ace = 0
forehand_winners = 0
backhand_winners = 0
net_winners = 0

double_faults = 0
forehand_errors = 0
backhand_errors = 0
net_errors = 0

def tennis_data(name):
    global ace, forehand_winners, backhand_winners, net_winners
    global double_faults, forehand_errors, backhand_errors, net_errors

    try:
        # Fetch your tennis data here, then pass it to render_template
        tennis_name = name  # captured from the URL
        # Remove all spaces from the name
        name = name.replace(" ", "")

        # Your URL will look something like this depending on the player's name structure
        url = f"https://www.tennisabstract.com/charting/{name}.html"
        tennis_link  = url

        # Check if URL is valid by making a request
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)

        # If URL doesn't exist (404) or other HTTP error, skip
        if response.status_code != 200:
            print(f"Skipping {tennis_name} - URL not valid (Status: {response.status_code})")
            return

        nummatches = fetch_matches(url)

        # Check if the page exists by validating nummatches or checking for valid data
        if nummatches is None or nummatches == 0 or nummatches == 1:
            print(f"Skipping {tennis_name} - no data available")
            return

        # Fetch unforced errors and winners data using functions
        olddata, newdata = fetch_tennis_data(url, display=False)
        olddata_4, newdata_4 = fetch_tennis_data_4(url, display=False)

        # Check if data was successfully retrieved
        if newdata is None or newdata_4 is None:
            print(f"Skipping {tennis_name} - could not fetch data")
            return

        winners_and_unforced_data = [newdata, newdata_4]
        #print(winners_and_unforced_data[0][1][1], winners_and_unforced_data[0][2][1], winners_and_unforced_data[0][3][1], winners_and_unforced_data[0][4][1], winners_and_unforced_data[1][1][1], winners_and_unforced_data[1][2][1], winners_and_unforced_data[1][3][1], winners_and_unforced_data[1][4][1])
        ace += int(winners_and_unforced_data[0][1][1])
        forehand_winners += int(winners_and_unforced_data[0][2][1])
        backhand_winners += int(winners_and_unforced_data[0][3][1])
        net_winners += int(winners_and_unforced_data[0][4][1])

        double_faults += int(winners_and_unforced_data[1][1][1])
        forehand_errors += int(winners_and_unforced_data[1][2][1])
        backhand_errors += int(winners_and_unforced_data[1][3][1])
        net_errors += int(winners_and_unforced_data[1][4][1])

    except Exception as e:
        print(f"Skipping {name} - Error: {e}")
        return

def format_winners_data():
    """
    Takes the winner counts and formats them into a list with percentages.
    Returns format: [['Winner Type', 'Count', 'Percentage'], ['Ace', count, 'X.XX%'], ...]
    """
    # Calculate total winners
    total_winners = ace + forehand_winners + backhand_winners + net_winners

    # Avoid division by zero
    if total_winners == 0:
        return [['Winner Type', 'Count', 'Percentage'],
                ['Ace', 0, '0.00%'],
                ['Forehand', 0, '0.00%'],
                ['Backhand', 0, '0.00%'],
                ['Net', 0, '0.00%']]

    # Calculate percentages
    ace_pct = (ace / total_winners) * 100
    forehand_pct = (forehand_winners / total_winners) * 100
    backhand_pct = (backhand_winners / total_winners) * 100
    net_pct = (net_winners / total_winners) * 100

    # Format the data
    formatted_data = [
        ['Winner Type', 'Count', 'Percentage'],
        ['Ace', ace, f'{ace_pct:.2f}%'],
        ['Forehand', forehand_winners, f'{forehand_pct:.2f}%'],
        ['Backhand', backhand_winners, f'{backhand_pct:.2f}%'],
        ['Net', net_winners, f'{net_pct:.2f}%']
    ]

    return formatted_data

def format_errors_data():
    """
    Takes the unforced error counts and formats them into a list with percentages.
    Returns format: [['Unforced Error', 'Count', 'Percentage'], ['Double Fault', count, 'X.XX%'], ...]
    """
    # Calculate total errors
    total_errors = double_faults + forehand_errors + backhand_errors + net_errors

    # Avoid division by zero
    if total_errors == 0:
        return [['Unforced Error', 'Count', 'Percentage'],
                ['Double Fault', 0, '0.00%'],
                ['Forehand', 0, '0.00%'],
                ['Backhand', 0, '0.00%'],
                ['Net', 0, '0.00%']]

    # Calculate percentages
    df_pct = (double_faults / total_errors) * 100
    forehand_pct = (forehand_errors / total_errors) * 100
    backhand_pct = (backhand_errors / total_errors) * 100
    net_pct = (net_errors / total_errors) * 100

    # Format the data
    formatted_data = [
        ['Unforced Error', 'Count', 'Percentage'],
        ['Double Fault', double_faults, f'{df_pct:.2f}%'],
        ['Forehand', forehand_errors, f'{forehand_pct:.2f}%'],
        ['Backhand', backhand_errors, f'{backhand_pct:.2f}%'],
        ['Net', net_errors, f'{net_pct:.2f}%']
    ]

    return formatted_data

def save_formatted_data_to_csv():
    """
    Saves the formatted data (ATP and WTA winners and errors) to individual CSV files.
    """
    import csv

    # Save ATP winners data
    with open('atp_winners_formatted.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(atp_winners_formatted)

    # Save ATP errors data
    with open('atp_errors_formatted.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(atp_errors_formatted)

    # Save WTA winners data
    with open('wta_winners_formatted.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(wta_winners_formatted)

    # Save WTA errors data
    with open('wta_errors_formatted.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(wta_errors_formatted)

    print("\nData saved to CSV files:")
    print("- atp_winners_formatted.csv")
    print("- atp_errors_formatted.csv")
    print("- wta_winners_formatted.csv")
    print("- wta_errors_formatted.csv")

# Initialize the formatted data variables with default values
atp_winners_formatted = [['Winner Type', 'Count', 'Percentage'],
                         ['Ace', 0, '0.00%'],
                         ['Forehand', 0, '0.00%'],
                         ['Backhand', 0, '0.00%'],
                         ['Net', 0, '0.00%']]

atp_errors_formatted = [['Unforced Error', 'Count', 'Percentage'],
                        ['Double Fault', 0, '0.00%'],
                        ['Forehand', 0, '0.00%'],
                        ['Backhand', 0, '0.00%'],
                        ['Net', 0, '0.00%']]

wta_winners_formatted = [['Winner Type', 'Count', 'Percentage'],
                         ['Ace', 0, '0.00%'],
                         ['Forehand', 0, '0.00%'],
                         ['Backhand', 0, '0.00%'],
                         ['Net', 0, '0.00%']]

wta_errors_formatted = [['Unforced Error', 'Count', 'Percentage'],
                        ['Double Fault', 0, '0.00%'],
                        ['Forehand', 0, '0.00%'],
                        ['Backhand', 0, '0.00%'],
                        ['Net', 0, '0.00%']]

# Only run scraping when this file is executed directly (not when imported)
if __name__ == "__main__":
    import csv
    from Tennis_Abstract_Scraping_v2 import *
    from Name_scrape_top_100 import *

    # Read 100 names from atp_top_100.csv and process them
    with open('atp_top_100.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if count >= 100:
                break
            player_name = row['name']
            print(f"Processing {player_name}...")
            tennis_data(player_name)
            count += 1

    print(f"\nTotal Aces: {ace}")
    print(f"Total Forehand Winners: {forehand_winners}")
    print(f"Total Backhand Winners: {backhand_winners}")
    print(f"Total Net Winners: {net_winners}")
    print(f"\nTotal Double Faults: {double_faults}")
    print(f"Total Forehand Errors: {forehand_errors}")
    print(f"Total Backhand Errors: {backhand_errors}")
    print(f"Total Net Errors: {net_errors}")

    # Format and display the winners data
    winners_formatted = format_winners_data()
    print("\n\nFormatted Winners Data:")
    print(winners_formatted)

    # Format and display the errors data
    errors_formatted = format_errors_data()
    print("\n\nFormatted Errors Data:")
    print(errors_formatted)

    atp_winners_formatted = winners_formatted
    atp_errors_formatted = errors_formatted

    # Reset counters for WTA
    ace = 0
    forehand_winners = 0
    backhand_winners = 0
    net_winners = 0
    double_faults = 0
    forehand_errors = 0
    backhand_errors = 0
    net_errors = 0

    # Read 100 names from wta_top_100.csv and process them
    with open('wta_top_100.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if count >= 100:
                break
            player_name = row['name']
            print(f"Processing {player_name}...")
            tennis_data(player_name)
            count += 1

    print(f"\nTotal Aces: {ace}")
    print(f"Total Forehand Winners: {forehand_winners}")
    print(f"Total Backhand Winners: {backhand_winners}")
    print(f"Total Net Winners: {net_winners}")
    print(f"\nTotal Double Faults: {double_faults}")
    print(f"Total Forehand Errors: {forehand_errors}")
    print(f"Total Backhand Errors: {backhand_errors}")
    print(f"Total Net Errors: {net_errors}")

    # Format and display the winners data
    winners_formatted = format_winners_data()
    print("\n\nFormatted Winners Data (WTA):")
    print(winners_formatted)

    # Format and display the errors data
    errors_formatted = format_errors_data()
    print("\n\nFormatted Errors Data (WTA):")
    print(errors_formatted)

    wta_winners_formatted = winners_formatted
    wta_errors_formatted = errors_formatted

    # Save all formatted data to CSV files
    save_formatted_data_to_csv()