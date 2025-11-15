import requests
from config import ODDS_API_KEY, ODDS_API_BASE_URL


def fetch_nba_odds():
    
    """ Fetech NBA odds from The Odds API """

    url = f'{ODDS_API_BASE_URL}/sports/basketball_nba/odds/'

#Example Response'
    
    params = {
        'apiKey' : ODDS_API_KEY,
        'regions' : 'us',
        'markets' : 'h2h',
        'oddsFormat' : 'american'

    }

    try:
        # check if API key is missing
        if not ODDS_API_KEY:
            print("Error: ODDS_API_KEY is not set. Check you .env file.")
            return []
            
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status() # Raises error for bad status
        try:
            return response.json()
        except ValueError:
            print("Error: Recieved invalid JSON from odds API.")
        return []
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching odds: {e}")
        return []