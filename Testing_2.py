
from winners_and_unforced_from_top_100 import *


# Read 100 names from atp_top_100.csv and process them
import csv

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