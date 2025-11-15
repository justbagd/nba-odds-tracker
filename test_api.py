import requests

# Hardcode the API key for now
API_KEY = ''

# The Odds API endpoint for NBA
url = f'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads'

print(f"Calling API...\n")

# Make the request
response = requests.get(url)

# Check if it worked
if response.status_code == 200:
    games = response.json()
    
    print(f"Found {len(games)} NBA games with odds:\n")
    
    # Loop through each game
    for game in games:
        home = game['home_team']
        away = game['away_team']
        
        print(f"{away} @ {home}")
        
        # Show odds from first bookmaker
        if game['bookmakers']:
            bookmaker = game['bookmakers'][0]
            print(f"  Bookmaker: {bookmaker['title']}")
            
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':  # Moneyline odds
                    for outcome in market['outcomes']:
                        print(f"    {outcome['name']}: {outcome['price']}")
        
        print()  # Blank line between games
else:
    print(f"Error: {response.status_code}")
    print(response.text)