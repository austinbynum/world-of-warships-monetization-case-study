import requests
import pandas as pd

# 1. Define your API parameters
APP_ID = 'cf3f6bed953f34a84105e228afb554ee' 

# Wargaming API URL structure: http(s)://<server>/<API_name>/<group>/<method>/? [16]
# Using the North American (NA) server for the Encyclopedia Ships method
URL = f"https://api.worldofwarships.com/wows/encyclopedia/ships/"

# 2. Set up the request parameters
params = {
    'application_id': APP_ID,
    'language': 'en', # [17]
    # 'fields' parameter narrows down the data so you don't pull unnecessary JSON bloat [18, 19]
    'fields': 'ship_id,name,tier,type,nation,is_premium'
}

print("Fetching ship data from Wargaming API...")

# 3. Make the GET request
response = requests.get(URL, params=params)
data = response.json()

# 4. Verify Data Integrity (Check if status is 'ok') [5]
if data.get('status') == 'ok':
    print("Data fetched successfully! Processing...")
    
    # The 'data' key contains a dictionary of ships, we want to extract the values
    ships_dict = data.get('data', {})
    
    # Convert the dictionary of ship objects into a list
    ships_list = list(ships_dict.values())
    
    # 5. Load into a Pandas DataFrame
    df_ships = pd.DataFrame(ships_list)
    
    # Display the first 5 rows to verify
    print(df_ships.head())
    
    # 6. Save to CSV for Phase 3 (Process)
    output_filename = "wows_ship_encyclopedia.csv"
    df_ships.to_csv(output_filename, index=False)
    print(f"Data saved successfully to {output_filename}")
    
else:
    # Error handling based on WG API error format [5]
    error_msg = data.get('error', {}).get('message', 'Unknown Error')
    print(f"API Request Failed. Error: {error_msg}")