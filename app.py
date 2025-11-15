from flask import Flask, render_template
from api_client import fetch_nba_odds
from config import DEBUG


# create app instance
app = Flask(__name__)

#  convert american to implied probability
def american_to_prob(odds):
    if odds > 0:
        probability = 100 / (odds + 100)
    else:
        probability = abs(odds) / ( abs(odds) + 100)
    return probability * 100

# Homepage
@app.route('/')
def home():
    
    """ Fetch API Data """
    games = fetch_nba_odds()


    # convert american to implied prob
    for game in games:
        
        # collect odds for best-value 
        away_list = []
        home_list = []
        
        
        for book in game.get("bookmakers", []):
            for market in book.get("markets", []):
                if market["key"] == "h2h":

                    # get price
                    away_price = market["outcomes"][0]["price"]
                    home_price = market["outcomes"][1]["price"]
                    
                    away_list.append(away_price)
                    home_list.append(home_price)
                    
            best_away = max(away_list)
            best_home = max(home_list)
            
            
        for book in game.get("bookmakers", []):
            for market in book.get("markets", []):
                if market["key"] == "h2h":
                    
                    # get price
                    away_price = market["outcomes"][0]["price"]
                    home_price = market["outcomes"][1]["price"]
                    
                    # convert to probability and add to list
                    market["outcomes"][0]["prob"] = format(american_to_prob(away_price), ",.2f")
                    market["outcomes"][1]["prob"] = format(american_to_prob(home_price), ",.2f")
                    
                    market["outcomes"][0]["is_best"] = (away_price == best_away)
                    market["outcomes"][1]["is_best"] = (home_price == best_away)

        # pass data to HTML
    return render_template("index.html", games=games)
# About page
@app.route('/about')
def about_page():
    """About page for the app."""
    return 'This is the about page'

## Run the app
if __name__ == '__main__':
    app.run(debug=DEBUG)

