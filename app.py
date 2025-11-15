from flask import Flask, render_template
from api_client import fetch_nba_odds
from config import DEBUG
from database import init_db, save_odds


# initialize DB on startup
init_db()


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
    
    # print(games)


    # Loop through each game
    for game in games:
        
        # collect odds for best-value 
        away_list = []
        home_list = []
        
        
       # generate unique game_id 
        game_id = f"{game['away_team']}_{game['home_team']}_{game['commence_time']}"
        
        

        # collect odds for comparison
        for book in game.get("bookmakers", []):
            
            for market in book.get("markets", []):
                if market["key"] == "h2h":

                    # get price
                    away_price = market["outcomes"][0]["price"]
                    home_price = market["outcomes"][1]["price"]
                    
                    away_list.append(away_price)
                    home_list.append(home_price)
        
        # take the highest positive number
        best_away = max(away_list)
        best_home = max(home_list)
            
        # conver american to implied prob
        for book in game.get("bookmakers", []):
            for market in book.get("markets", []):
                if market["key"] == "h2h":
                    
                    # get price
                    away_price = market["outcomes"][0]["price"]
                    home_price = market["outcomes"][1]["price"]
                    
                    
                    # convert to prob
                    away_prob = american_to_prob(away_price)
                    home_prob = american_to_prob(home_price)
                    
                    # add to list
                    market["outcomes"][0]["prob"] = format(away_prob, ",.2f")
                    market["outcomes"][1]["prob"] = format(home_prob, ",.2f")
                    
                    # highlight best odds
                    market["outcomes"][0]["is_best"] = (away_price == best_away)
                    market["outcomes"][1]["is_best"] = (home_price == best_home)
                    
                    save_odds(
                        game_id,
                        book["title"],
                        market["outcomes"][0]["name"],
                        away_price,
                        away_prob
                    )
                    
                    save_odds(game_id,
                              book["title"],
                              market["outcomes"][1]["name"],
                              home_price,
                              home_prob)

        # pass data to HTML
    return render_template("index.html", games=games)
    
    # return game_id
# About page
@app.route('/about')
def about_page():
    """About page for the app."""
    return 'This is the about page'

## Run the app
if __name__ == '__main__':
    app.run(debug=DEBUG)

