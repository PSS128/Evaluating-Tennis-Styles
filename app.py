from flask import Flask, render_template, request, jsonify
import csv
import os
from Tennis_Abstract_Scraping_v2 import (
    fetch_tennis_data_2,
    fetch_tennis_data,
    fetch_tennis_data_3,
    fetch_tennis_data_4,
    display_percentage_difference,
    fetch_matches,
    find_keywords
)

app = Flask(__name__)

# Read tennis players from CSV files in csv_files folder
tennis_players = []
csv_files_dir = os.path.join(os.path.dirname(__file__), 'csv_files')

# Try to load from multiple CSV files
csv_file_names = ['all_atp_players.csv', 'all_wta_players.csv', 'atp_top_100.csv', 'wta_top_100.csv', 'names.csv']

for csv_file_name in csv_file_names:
    csv_path = os.path.join(csv_files_dir, csv_file_name)
    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if row:  # Check row is not empty
                        full_name = row[0]
                        if full_name not in tennis_players:  # Avoid duplicates
                            tennis_players.append(full_name)
        except Exception as e:
            print(f"Error reading {csv_file_name}: {e}")

# If no players loaded, add a default empty list
if not tennis_players:
    print("Warning: No tennis players loaded from CSV files")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("term")
    search_result = [player for player in tennis_players if query.lower() in player.lower()]
    return jsonify(search_result)




@app.route("/tennis_data/<name>", methods=["GET"])
def tennis_data(name):
    # Fetch your tennis data here, then pass it to render_template
    tennis_name = name  # captured from the URL
    # Remove all spaces from the name
    name = name.replace(" ", "")
    
    # Your URL will look something like this depending on the player's name structure
    url = f"https://www.tennisabstract.com/charting/{name}.html"
    tennis_link  = url
    nummatches = fetch_matches(url)
    # Fetch all the data using your functions
    olddata_2, newdata_2 = fetch_tennis_data_2(url, display=False)
    olddata_3, newdata_3 = fetch_tennis_data_3(url, display=False)
    olddata, newdata = fetch_tennis_data(url, display=False)
    olddata_4, newdata_4 = fetch_tennis_data_4(url, display=False)

    percentdata_2 = display_percentage_difference(olddata_2, newdata_2, "Points by Rally Length")
    percentdata_3 = display_percentage_difference(olddata_3, newdata_3, "Shot Frequency")
    percentdata = display_percentage_difference(olddata, newdata, "Winner Type")
    percentdata_4 = display_percentage_difference(olddata_4, newdata_4, "Unforced Error")

    all_percentage_data = [percentdata_2, percentdata_3, percentdata, percentdata_4]
    keywords = find_keywords(all_percentage_data)
    
    # Return the render template with all your data
    return render_template("tennis_data.html", 
                        olddata_2=olddata_2, newdata_2=newdata_2, percentdata_2=percentdata_2, 
                        olddata_3=olddata_3, newdata_3=newdata_3, percentdata_3=percentdata_3,
                        olddata=olddata, newdata=newdata, percentdata=percentdata,
                        olddata_4=olddata_4, newdata_4=newdata_4, percentdata_4=percentdata_4, 
                        tennis_name=tennis_name, tennis_link = tennis_link, nummatches = nummatches,
                        keywords=keywords)



if __name__ == "__main__":
    app.run()


