from flask import Flask, render_template, request, jsonify
import csv
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

# Read tennis players from a CSV file
tennis_players = []
with open("names.csv", "r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        full_name = row[0]
        tennis_players.append(full_name)

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
    url = f"http://www.tennisabstract.com/charting/{name}.html"
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


