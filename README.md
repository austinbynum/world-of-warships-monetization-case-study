# World of Warships Monetization Case Study

## 📝 Project Overview
This project serves as an end-to-end data analytics case study exploring the monetization strategies and in-game economy of World of Warships. Byprogrammatically extracting ship attributes and player performance statistics directly from the Wargaming.net Public API, this study investigates the behavioral and economic differences between players using standard Tech Tree ships versus purchasable Premium ships.
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

## 💡 Phase 4: Analyze (Key Findings)


## 📈 Phase 5: Share (Visualizations)


## 🚀 Phase 6: Act (Strategic Recommendations)


---
### 👨‍💻 Connect with Me
* **Portfolio:** [austinbynum.com](https://www.austinbynum.com)
* **GitHub:** [github.com/austinbynum](https://github.com/austinbynum)
* **LinkedIn:** [linkedin.com/in/austin-bynum-323228315](https://www.linkedin.com/in/austin-bynum-323228315/)
* **Kaggle:** [kaggle.com/austinbynumahs10](https://www.kaggle.com/austinbynumahs10)
