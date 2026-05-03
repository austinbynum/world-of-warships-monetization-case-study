import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# 1. Define your API parameters
# This pulls the ID from your local .env file securely
APP_ID = os.getenv('WG_APP_ID') 

URL = "https://api.worldofwarships.com/wows/encyclopedia/ships/"

# Create an empty list to store all the ships across multiple pages
all_ships_list = []
page_no = 1 

print("Fetching ship data from Wargaming API...")

# 2. Loop through pages until no more ships are returned
while True:
    params = {
        'application_id': APP_ID,
        'language': 'en',
        'fields': 'ship_id,name,tier,type,nation,is_premium',
        'page_no': page_no # Dynamic page number
    }
    
    response = requests.get(URL, params=params)
    data = response.json()
    
    # 3. Verify Data Integrity
    if data.get('status') == 'ok':
        # The 'data' key contains a dictionary of ships on the current page
        ships_dict = data.get('data', {})
        
        # If the dictionary is empty, we have reached the last page. Break the loop.
        if not ships_dict:
            break
            
        # Add the current page's ships to our master list
        all_ships_list.extend(list(ships_dict.values()))
        
        print(f"Fetched page {page_no}...")
        page_no += 1 # Move to the next page for the next loop iteration
        
    else:
        error_msg = data.get('error', {}).get('message', 'Unknown Error')
        print(f"API Request Failed on page {page_no}. Error: {error_msg}")
        break

# 4. Load the compiled list into a Pandas DataFrame
df_ships = pd.DataFrame(all_ships_list)

print(f"\nSuccess! Total ships fetched: {len(df_ships)}")

# 5. Save to your processed data folder using forward slashes
output_filename = "../01_raw_data/wows_ship_encyclopedia.csv"

# Optional: Ensure the directory exists before saving (avoids FileNotFoundError)
os.makedirs(os.path.dirname(output_filename), exist_ok=True)

df_ships.to_csv(output_filename, index=False)
print(f"Data saved successfully to {output_filename}")