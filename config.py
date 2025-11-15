import os
from dotenv import load_dotenv

# Load enviroment variales from .env file
load_dotenv()

# API Config
ODDS_API_KEY = os.getenv('ODDS_API_KEY')
ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4'

# App Config
DEBUG = True

