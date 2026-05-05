# World of Warships Monetization Case Study

## 📝 Project Overview
This project serves as an end-to-end data analytics case study exploring the monetization strategies and in-game economy of World of Warships. By programmatically extracting ship attributes and player performance statistics directly from the Wargaming.net Public API, this study investigates the behavioral and economic differences between players using standard Tech Tree ships versus purchasable Premium ships.
Using a custom data pipeline built with Python, Google BigQuery (SQL), and Power BI, I processed and analyzed engagement metrics—such as usage rates, win rates, and base experience generation—to uncover actionable trends in player purchasing patterns. The resulting insights are designed to help Wargaming's product and balancing teams optimize future Premium ship releases to maximize both long-term player retention and revenue.

## 🎯 Phase 1: Ask
**Business Task:** To analyze the usage rates, in-game performance, and player engagement levels of Premium ships compared to Tech Tree ships. By identifying which tiers, classes, and specific types of Premium ships drive the highest engagement and ownership, I will provide data-driven recommendations on what types of Premium ships Wargaming should focus on releasing next to maximize monetization and player retention.

**Key Stakeholders:**
* **Wargaming's Monetization and Product Teams:** They need to understand player purchasing patterns and engagement to decide how to price ships and what types of bundles or Premium ships to sell for Doubloons (the primary cash currency).
* **Game Balancers / Development Team:** They need to ensure that the Premium ships being released to drive revenue are not negatively impacting the overall game balance (e.g., ships that are heavily played but have disproportionately high or low win rates).

## 🛠️ Technical Toolkit
* **Python:** Fetch raw data from Wargaming API.
* **Excel/Sheets:** Cleaning and summarization.
* **SQL:** Processing and combining into one table.
* **Power BI:** Advanced and interactive visualizations.

## 📂 Repository Structure
* `01_raw_data/`: Untouched JSON/CSV output fetched from Wargaming API.
* `02_processed_data/`: CSV files of raw data cleaned and summarized, ready for final reporting.
* `03_scripts_notebooks/`: Python script to collect data and SQL script to process data
* `04_visualizations/`: Final charts in PDF and PNG formats.
* `05_reports/`: Executive summary and final project PDF.

## 📊 Phase 2 & 3: Prepare & Process (Data & Methodology)
**Data Sources:** The data for this case study is extracted directly from the **Wargaming.net Public API**, a first-party developer service providing live access to game content and player statistics. Specifically, this analysis utilizes two main API endpoints:
* **Encyclopedia API (`/wows/encyclopedia/ships/`):** Used to extract static ship attributes, such as tier, nation, ship class, and the critical `is_premium status`.
* **Warships API (`/wows/ships/stats/`):** Used to extract historical player performance data on specific ships, including usage rates, win/loss ratios, and base experience generated.
* **Players API (`/wows/account/list/`):** Due to limitations of the Warships API, I need to contruct a respresentative sample without brute-forcing random player IDs. To accomplish this, the data collection script programmatically queries this endpoint using a predefined list of 10 common username prefixes. This extracts 1,000 valid `account_id`s, which are then used to fetch individual ship performance records.

**Data Integrity:**
* **Credibility (ROCCC):** I am pulling data directly from Wargaming's own servers, so the data is first-party, reliable, original, and current. It is also unbiased because it reflects the exact database used to run the game.
* **Technical Integrity:**
	* Checking the API response header for `status`: `ok`, which confirms the request was processed successfully without returning an `error` dictionary.
	* Managing API rate limits (standalone applications are limited to 10 requests per second) to ensure data pull is not truncated or missing record.
	* Checking final output (e.g., CSV files) for missing or null values—such as test ships or newly released ships that might lack complete public statistics.

**Data Privacy & Licensing:**
* **Licensing:** I am operating under Wargaming's limited, non-exclusive, revocable license to use their API data for this publicly available application/analysis.
* **Copyright Notice:** Wargaming's policy requires the inclusion of the notice, _"© Wargaming.net. All rights reserved"_.
* **Attribution:** The source of the data is the [official World of Warships website](https://worldofwarships.com/) and this project is not affiliated with or endorsed by Wargaming.
* **Privacy:** No personal passwords were collected and only the data necessary for the analysis was collected.

**How to Reproduce the Data Collection:** To reproduce the API extraction process and run the Python scripts locally, you will need to set up your environment and obtain your own API credentials. Follow these steps:
1. Install Required Python Packages: The data collection scripts utilize external libraries that must be installed via your computer's terminal or command prompt (do not run this command inside the Python script). Open your terminal and run the following command: `pip install requests pandas python-dotenv`
2. Obtain a Wargaming Application ID: Access to the Wargaming.net API requires a personal Application ID. Register for a free developer account at the [Wargaming Developer Room](https://developers.wargaming.net/) and create a "Standalone" application to generate your key. 
3. Set Up Your Environment Variable: To keep your Application ID secure and comply with Wargaming's Terms of Use, the Python script uses the `python-dotenv` package to load the key as a local environment variable. 
	* In the root directory of your cloned repository, create a plain text file named exactly `.env`.
	* Add your Application ID to the file in this exact format: `WG_APP_ID=your_application_id_here`
	* **Important:** Ensure your `.env` file is listed in your `.gitignore` file so your secret key is never pushed to your public repository!
	
**Data Volume & Sampling Note:** The default configuration of the data collections script uses 10 common username prefixes to query the `/wows/account/list/` endpoint, extracting 983 valid `account_id`s. Of those valid `account_id`s, 527 returned stats. This default sample yields 9,810 individual ship performance records. While this is sufficient for the scope of this case study, it suggests a high volume of either:
* **Hidden Profiles:** Wargaming allows players to hide their statistics. The API explicitly tracks a hidden_profile status, and if a player has their profile set to private, the API will not return their ship performance data.
* **Zero PvP Battles:** The Python script was specifically designed to filter out ships with 0 Random Battles (`pvp`) played. Many accounts may only play Co-op battles (which the game actively incentivizes with discounted service costs) or may have simply created an account without ever playing a match.

**Data Cleaning & Preparation Steps:** Because the data was extracted programmatically via API, it lacked traditional errors like null values or misaligned columns. Using Google Sheets/Excel, the following cleaning tasks were completed:
* **`wows_ship_encyclopedia.csv`:**
	1. Removed empty rows at the end of the data.
	2. Ensured accurate data formatting.
	3. Sorting `name` alphabetically, I found some ship names inside brackets, which indicates the player did not own the ship, but rather rented it. Because the business task is specifically focused on comparing standard Tech Tree ships to purchasable Premium ships, these temporary rentals were removed.
	4. Two ships were listed twice ("Schlieffen" & "Vrijheid") with different ship IDs. This was determined to be caused by developers releasing beta versions of the ships to be tested, changing the `ship_id` to release the final version of the ship. I resolved this by searching `wows_player_ship_stats.csv` for the IDs. Only 1 of the "Schlieffen" ships were played, so I deleted the others as they would have been removed when I JOIN the tables later.
	5. Added `event` column to indicate ships purchased during a special event or ones offered with special variants.
* **`wows_player_ship_stats.csv`:**
	1. Removed empty rows at the end of the data.
	2. Ensured accurate data formatting.

## 💡 Phase 4: Analyze (Key Findings)


## 📈 Phase 5: Share (Visualizations)


## 🚀 Phase 6: Act (Strategic Recommendations)


---
### 👨‍💻 Connect with Me
* **Portfolio:** [austinbynum.com](https://www.austinbynum.com)
* **GitHub:** [github.com/austinbynum](https://github.com/austinbynum)
* **LinkedIn:** [linkedin.com/in/austin-bynum-323228315](https://www.linkedin.com/in/austin-bynum-323228315/)
* **Kaggle:** [kaggle.com/austinbynumahs10](https://www.kaggle.com/austinbynumahs10)
