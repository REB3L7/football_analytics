# ⚽ Football Analytics & Scouting Platform

### Premier League 2025/26 | Python • PostgreSQL • SQL • Tableau

An end-to-end football analytics platform built to analyze player performance, evaluate attacking efficiency, and identify standout players using data-driven scouting models.

The project combines Python-based data processing, PostgreSQL database management, SQL analytics, and interactive Tableau visualizations to transform raw football statistics into actionable insights.

**Dataset:** 414 Premier League players across 20 clubs  
**Season:** 2025/26 (early-season snapshot)

## 🌐 Live Interactive Dashboard

### Premier League Scouting & Performance Dashboard

**[📊 Explore the Tableau Dashboard](https://public.tableau.com/app/profile/roti.ojo.akinkunmi/viz/PremierLeagueScoutingPerformanceDashboard202526/ENGLISHPREMIERLEAGUESCOUTINGPERFORMANCEDASHBOARD)**

The interactive Tableau dashboard provides four complementary views of Premier League player performance.

### Dashboard Features

**1. Top 10 Goalscorers**
- Ranks the league's leading goalscorers.
- Displays total goals scored by each player.
- Highlights early-season attacking performance.

**2. Goals vs. Expected Goals (xG)**
- Compares actual goals against expected goals.
- Identifies players outperforming or underperforming their expected output.
- Uses a reference line to visualize finishing efficiency.

**3. Scouting Leaderboard**
- Ranks players using percentile-based scouting scores.
- Supports three selectable scouting categories:
  - Goalscorer
  - Creator
  - All-Round
- Includes interactive team filtering and player rankings.

**4. Player Comparison**
- Allows users to select and compare two players.
- Compares seven performance metrics:
  - Assists per 90
  - Games
  - Goals per 90
  - Expected assists (xA)
  - Expected assists per 90
  - Expected goals (xG)
  - Expected goals per 90

The dashboard allows users to explore performance trends, compare players, and evaluate scouting results through an interactive interface.

---

## 🎯 Project Objectives

This project was developed to:

- Build an end-to-end football analytics workflow.
- Practice data extraction, transformation, and loading (ETL).
- Design and query a relational PostgreSQL database.
- Apply SQL analytics to real-world sports data.
- Evaluate player performance using standardized metrics.
- Develop data-driven scouting and ranking models.
- Create interactive visualizations for exploring results.
- Demonstrate practical data engineering and analytics skills.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing, automation, and ETL |
| Pandas | Data cleaning and transformation |
| NumPy | Numerical analysis |
| PostgreSQL | Relational database management |
| SQL | Analytical queries, window functions, and rankings |
| psycopg | Python-to-PostgreSQL connectivity |
| Matplotlib | Static performance visualizations |
| Tableau Public | Interactive dashboards and player comparisons |
| Git & GitHub | Version control and project documentation |

---

## 🏗️ System Architecture

The platform follows a data analytics pipeline:

```text
Football Performance Dataset
            |
            v
    Python Data Processing
            |
            v
     Data Cleaning & ETL
            |
            v
      PostgreSQL Database
            |
            v
     SQL Analytical Views
            |
            v
    Scouting Scoring Models
            |
            v
     Visualization Layer
            |
       +----+----+
       |         |
       v         v
   Matplotlib  Tableau
     Charts    Dashboard
```

### Workflow

1. Load player performance data into Python.
2. Clean and standardize player statistics using Pandas.
3. Transform the dataset into structured relational tables.
4. Load the processed data into PostgreSQL.
5. Execute SQL queries to calculate performance metrics.
6. Generate scouting rankings using percentile-based models.
7. Export analytical views for visualization.
8. Build static charts and an interactive Tableau dashboard.

---

## 🗄️ Database Design

The PostgreSQL database organizes football data into three main tables.

### Teams

Stores information about Premier League clubs.

### Players

Stores player information, including player identifiers and team relationships.

### Player Statistics

Stores individual player performance metrics, including:

- Appearances
- Minutes played
- Goals
- Assists
- Shots
- Key passes
- Expected goals (xG)
- Expected assists (xA)

This relational structure supports analytical queries and player-level performance comparisons.

---

## 📈 Performance Metrics

The platform calculates standardized statistics to compare players more effectively.

### Goals per 90 Minutes

```text
Goals per 90 = (Goals / Minutes Played) × 90
```

### Assists per 90 Minutes

```text
Assists per 90 = (Assists / Minutes Played) × 90
```

### Expected Goals per 90 Minutes

```text
xG per 90 = (Expected Goals / Minutes Played) × 90
```

### Expected Assists per 90 Minutes

```text
xA per 90 = (Expected Assists / Minutes Played) × 90
```

### Goals Minus Expected Goals

```text
Goals - xG
```

This metric helps identify players scoring above or below their expected goal totals.

Per-90 metrics help account for differences in playing time when evaluating performance.

---

## 🔍 Scouting & Ranking Models

The platform implements three scouting categories to evaluate attacking players.

### 1. Goalscorer Score

Evaluates players based on their goalscoring performance.

### 2. Creator Score

Evaluates players based on their ability to generate attacking opportunities and contribute assists.

### 3. All-Round Score

Evaluates players across multiple attacking performance metrics.

### Scoring Methodology

The scouting models use percentile-based scoring to compare players within the eligible dataset.

SQL window functions are used to calculate rankings and generate leaderboards.

Players must meet a minimum playing-time threshold of **270 minutes** to qualify for the scouting leaderboard.

This helps reduce the influence of extremely small samples.

### Interactive Scouting

The Tableau dashboard allows users to switch between Goalscorer, Creator, and All-Round scores without rebuilding the visualization.

---

## 📊 Data Visualizations

The project includes both Python-generated visualizations and an interactive Tableau dashboard.

### Python Visualizations

Matplotlib is used to explore player performance through visualizations such as:

- Goals vs. expected goals
- Player comparison charts
- Performance distributions
- Scouting-related comparisons

### Tableau Dashboard

The Tableau dashboard extends the project by providing interactive visual analysis.

Users can:

- Explore top goalscorers.
- Evaluate goalscoring efficiency.
- Filter scouting rankings by club.
- Switch between scouting categories.
- Compare individual players.
- Examine performance metrics through interactive charts.

**[Open the Interactive Tableau Dashboard](https://public.tableau.com/app/profile/roti.ojo.akinkunmi/viz/PremierLeagueScoutingPerformanceDashboard202526/ENGLISHPREMIERLEAGUESCOUTINGPERFORMANCEDASHBOARD)**

---

## 📁 Project Structure

The project is organized around the following components:

```text
football-analytics/
|
├── data/
│   └── tableau/
│       ├── player_performance.csv
│       └── scouting_leaderboard.csv
│
├── README.md
├── requirements.txt
│
├── Python data processing and ETL scripts
├── PostgreSQL database and SQL queries
├── Scouting analysis and ranking models
└── Data visualizations
```

The Tableau CSV files are generated from PostgreSQL analytical views.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/REB3L7/football_analytics.git
cd football_analytics
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Install PostgreSQL and create a database:

```bash
createdb football_analytics
```

Configure the database connection in the project's Python scripts as required.

### 5. Run the Data Pipeline

Execute the project's data-processing and database-loading scripts in the order documented in the source code.

### 6. Explore the Results

Run the SQL analytical queries and generate the project's visualizations.

Alternatively, explore the published Tableau dashboard directly:

**[View Dashboard](https://public.tableau.com/app/profile/roti.ojo.akinkunmi/viz/PremierLeagueScoutingPerformanceDashboard202526/ENGLISHPREMIERLEAGUESCOUTINGPERFORMANCEDASHBOARD)**

---

## 💡 Key Takeaways

This project demonstrates practical experience in:

- Building data processing pipelines using Python.
- Cleaning and transforming structured datasets.
- Designing and querying PostgreSQL databases.
- Applying SQL window functions to analytical problems.
- Developing percentile-based ranking systems.
- Standardizing performance metrics for meaningful comparisons.
- Creating static and interactive data visualizations.
- Communicating analytical results through dashboards.

It combines data engineering, SQL analytics, and business intelligence concepts within a football scouting application.

---

## ⚠️ Data Limitations

This project uses an **early-season snapshot of the 2025/26 Premier League season**, rather than complete season statistics.

As a result:

- Player rankings reflect the available snapshot.
- Performance metrics may change as additional matches are played.
- Small sample sizes can influence early-season results.
- Scouting scores are analytical indicators rather than definitive assessments of player ability.
- The dataset should not be interpreted as current live-season data.

The scouting leaderboard uses a minimum playing-time threshold to reduce some small-sample effects.

---

## 🔮 Future Improvements

Potential enhancements include:

- Automated data updates from football statistics APIs.
- Multi-season player performance comparisons.
- Position-specific scouting models.
- Additional defensive and possession-based metrics.
- More advanced player similarity analysis.
- Automated Tableau data refresh workflows.
- Predictive modeling for player performance.

---

## 👨‍💻 Author

**Olumoroti Ojo-Akinkunmi**

Information Technology | University of South Florida

- [LinkedIn](https://www.linkedin.com/in/olumoroti-ojo-akinkunmi/)
- [GitHub](https://github.com/REB3L7)
- [Tableau Dashboard](https://public.tableau.com/app/profile/roti.ojo.akinkunmi/viz/PremierLeagueScoutingPerformanceDashboard202526/ENGLISHPREMIERLEAGUESCOUTINGPERFORMANCEDASHBOARD)

---

*Built to explore the intersection of football, data engineering, analytics, and interactive visualization.*