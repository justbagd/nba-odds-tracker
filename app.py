from flask import Flask, render_template
from api_client import fetch_nba_odds
from config import DEBUG


# create app instance
app = Flask(__name__)

# Homepage
@app.route('/')
def home():

    """ Display NBA odds homepage """
    games = fetch_nba_odds()
    return render_template('index.html', games=games)

# About page
@app.route('/about')
def about_page():
    """About page for the app."""
    return 'This is the about page'

## Run the app
if __name__ == '__main__':
    app.run(debug=DEBUG)

