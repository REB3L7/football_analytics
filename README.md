⚽ Football Analytics & Scouting Platform

A Python and PostgreSQL-based analytics platform designed to evaluate Premier League player performance, compare attacking statistics, and identify players suited to different scouting profiles.

The project combines data engineering, relational database design, SQL analytics, and data visualization to demonstrate how football performance data can support scouting decisions.

Project Overview

The platform analyzes 414 Premier League players across 20 clubs using an early-season snapshot of the 2025/26 season.

It processes player statistics, calculates standardized performance metrics, and ranks qualifying forwards according to their attacking strengths.

Key Features

* Data Processing: Clean and transform football statistics using Python and pandas.
* PostgreSQL Database: Store player, team, and performance data in related tables.
* Performance Analytics: Calculate goals, assists, expected goals (xG), expected assists (xA), and per-90-minute metrics.
* Scouting Models: Rank forwards using percentile-based performance scores.
* Specialized Scouting: Evaluate players across three profiles: All-Round, Goalscorer, and Creator.
* Player Comparison: Generate visual comparisons of attacking metrics.
* SQL Analytics: Use joins, common table expressions, views, and window functions to produce scouting leaderboards.

Technology Stack

Technology	Purpose
Python	Data processing and analytics
pandas / NumPy	Data cleaning and calculations
PostgreSQL	Relational database
SQL	Performance analysis and scouting rankings
psycopg	Python–PostgreSQL integration
Matplotlib	Data visualization
Git / GitHub	Version control

Architecture

Football Statistics Dataset
           |
           v
     Python + pandas
     Data Cleaning
           |
           v
    PostgreSQL Database
           |
     +-----+------+
     |     |      |
   Teams Players Player Stats
     |     |      |
     +-----+------+
           |
           v
      SQL Analytics
           |
           v
   Scouting Score Models
           |
           v
  Leaderboards & Visualizations

Scouting Methodology

The platform evaluates forwards who have played at least 270 minutes.

Each player receives percentile-based scores across six attacking metrics:

* Goals per 90
* Assists per 90
* Expected goals per 90
* Expected assists per 90
* Shots per 90
* Key passes per 90

Three scouting profiles are calculated.

All-Round

Uses equal weighting across all six attacking metrics.

Goalscorer

Prioritizes goal production and shooting opportunities.

Metric	Weight
Goals	35%
Expected Goals	35%
Shots	20%
Assists	5%
Expected Assists	5%

Creator

Prioritizes chance creation and attacking playmaking.

Metric	Weight
Assists	30%
Expected Assists	30%
Key Passes	25%
Goals	10%
Expected Goals	5%

These weights are exploratory choices rather than a validated predictive model.

Example Results

The following results demonstrate how player rankings change across scouting profiles.

Player	All-Round Rank	Goalscorer Rank	Creator Rank
Erling Haaland	4	1	12
Richarlison	1	2	3
João Pedro	2	7	1

Results are based on the September 2025 data snapshot and should not be interpreted as full-season rankings.

Visualizations

Goals vs. Expected Goals

Player Comparison

Project Structure

football-analytics/
├── dashboards/
│   ├── goals_vs_xg.png
│   └── player_comparison.png
├── data/
│   ├── raw/
│   └── processed/
├── sql/
│   ├── player_performance.sql
│   ├── forward_scouting.sql
│   ├── specialized_scouting.sql
│   └── scouting_leaderboard.sql
├── src/
│   ├── explore_data.py
│   ├── player_analysis.py
│   ├── visualize_players.py
│   ├── player_scouting.py
│   ├── player_comparison.py
│   ├── database_setup.py
│   └── import_data.py
├── requirements.txt
├── .gitignore
└── README.md

Dataset

The project uses publicly available football statistics from the Understat player aggregation dataset.

Source: vibedatascience/understat_players_aggregated on GitHub.

Important limitation: The dataset used for the current analysis was collected on September 21, 2025, early in the Premier League season. Consequently, rankings reflect a small sample of matches and may change substantially as more data becomes available.

Players with multiple club associations may also require additional handling to attribute their statistics accurately.

Setup

1. Clone the repository

git clone https://github.com/REB3L7/football_analytics.git
cd football_analytics

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Download the dataset

Create the raw data directory and download the source CSV:

mkdir -p data/raw data/processed
curl -L \
  https://raw.githubusercontent.com/vibedatascience/understat_players_aggregated/main/understat_players_aggregated_2025_latest.csv \
  -o data/raw/premier_league_players.csv

The upstream dataset may have changed since the snapshot used for the example results.

5. Prepare PostgreSQL

Install and start PostgreSQL, then create a database named:

football_analytics

The current database scripts use a local PostgreSQL connection and may require updating the username in src/database_setup.py and src/import_data.py.

6. Process and import data

Run the scripts in order:

python src/explore_data.py
python src/player_analysis.py
python src/database_setup.py
python src/import_data.py

7. Create the SQL analytics views

psql football_analytics -f sql/player_performance.sql
psql football_analytics -f sql/forward_scouting.sql
psql football_analytics -f sql/specialized_scouting.sql
psql football_analytics -f sql/scouting_leaderboard.sql

8. Query the scouting leaderboard

SELECT
    player_name,
    team_name,
    goalscorer_rank,
    creator_rank
FROM vw_scouting_leaderboard
ORDER BY goalscorer_rank
LIMIT 10;

Future Improvements

* Build an interactive Power BI scouting dashboard.
* Incorporate additional seasons and updated player statistics.
* Expand scouting models to midfielders and defenders.
* Improve transfer handling and historical team assignments.
* Evaluate scouting weights using larger datasets.

Author

Roti Ojo-Akinkunmi

Information Technology | University of South Florida