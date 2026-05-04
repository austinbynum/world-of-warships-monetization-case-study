import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load the Wargaming Application ID securely
load_dotenv()
APP_ID = os.getenv('WG_APP_ID')

# Define API Endpoints
URL_ACCOUNT_LIST = "https://api.worldofwarships.com/wows/account/list/"
URL_SHIP_STATS = "https://api.worldofwarships.com/wows/ships/stats/"

# 1. Define the search terms to build our player sample
# DEFAULT: Quick extraction (Yields ~1,000 players and ~10,000 ship records)
search_terms = ['Admiral', 'Captain', 'Sniper', 'Ghost', 'Killer', 'Navy', 'Sailor', 'Pirate', 'Alpha', 'Bravo']

# OPTIONAL EXTENDED SAMPLE: For a much larger, randomized dataset (~50,000+ records)
# To use this larger sample, uncomment the line below and change the 'for' loop to iterate over 'extended_search_terms'
# extended_search_terms = ['Dar', 'Fox', 'Red', 'Blu', 'One', 'The', 'Pro', 'Sky', 'Sea', 'War', 'Bat', 'Gun', 'Ship', 'Top', 'Max', 'Big', 'Ice', 'Fire', 'Bad', 'Mad']

# Use a set to store account_ids to automatically prevent any duplicate players
account_ids = set() 

print("Step 1: Fetching account IDs using search terms...")

# 2. Loop through search terms to fetch valid account IDs
for term in search_terms:
    params = {
        'application_id': APP_ID,
        'search': term,
        'limit': 100,           # The API allows a maximum of 100 entries per request
        'type': 'startswith'    # Searches by initial characters of the player name
    }
    
    response = requests.get(URL_ACCOUNT_LIST, params=params)
    data = response.json()
    
    if data.get('status') == 'ok':
        players = data.get('data', [])
        for player in players:
            account_ids.add(player.get('account_id'))
        print(f"Fetched {len(players)} players for search term '{term}'")
    else:
        error_msg = data.get('error', {}).get('message', 'Unknown Error')
        print(f"Failed to fetch term '{term}'. Error: {error_msg}")
        
    # Respect the standalone application API rate limit (max 10 requests per second)
    time.sleep(0.15) 

print(f"\nSuccessfully gathered {len(account_ids)} unique account IDs.")
print("\nStep 2: Fetching ship statistics for each player (This will take approximately 10 minutes)...")

all_player_stats = []
processed_count = 0

# 3. Loop through each gathered account_id to fetch their ship performance stats
for account_id in account_ids:
    params = {
        'application_id': APP_ID,
        'account_id': account_id,
        'language': 'en'
    }
    
    response = requests.get(URL_SHIP_STATS, params=params)
    data = response.json()
    
    if data.get('status') == 'ok':
        # The data is nested under the specific account_id
        player_ships = data.get('data', {}).get(str(account_id), [])
        
        # Check if the player has public stats and has played ships
        if player_ships:
            for ship in player_ships:
                # We only want to extract the 'pvp' (Random Battles) statistics
                pvp_stats = ship.get('pvp', {})
                
                # Filter out ships with 0 battles to keep the dataset clean
                if pvp_stats and pvp_stats.get('battles', 0) > 0:
                    ship_data = {
                        'account_id': account_id,
                        'ship_id': ship.get('ship_id'),
                        'battles': pvp_stats.get('battles', 0),
                        'wins': pvp_stats.get('wins', 0),
                        'survived_battles': pvp_stats.get('survived_battles', 0),
                        'damage_dealt': pvp_stats.get('damage_dealt', 0),
                        'frags': pvp_stats.get('frags', 0),
                        'xp': pvp_stats.get('xp', 0)
                    }
                    all_player_stats.append(ship_data)
                    
    processed_count += 1
    # Print a progress update every 20 accounts
    if processed_count % 20 == 0:
        print(f"Processed {processed_count} / {len(account_ids)} accounts...")
        
    # Respect the API rate limit again for this loop
    time.sleep(0.15) 

# 4. Load compiled statistics into a Pandas DataFrame
df_stats = pd.DataFrame(all_player_stats)

# 5. Save to your processed data folder
output_filename = "../01_raw_data/wows_player_ship_stats.csv"
os.makedirs(os.path.dirname(output_filename), exist_ok=True)
df_stats.to_csv(output_filename, index=False)

print(f"\nSuccess! Total ship records fetched across all players: {len(df_stats)}")
print(f"Data saved successfully to {output_filename}")