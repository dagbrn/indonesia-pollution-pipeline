# INDONESIA AIR POLLUTION DATA PIPELINE

**ETL (Extract, Transform, Load) pipeline** that collects real-time air quality data from OpenWeather API, transforms it, and loads it into PostgreSQL database.

## Project Overview

This project demonstrates data engineering practices including:
- API integration with error handling
- Data validation and quality checks
- Immutable data architecture
- Environment-based configuration management
- Comprehensive logging and monitoring
- Type hints and proper code structure
- Containerized deployment with Docker

## Features

### Data Sources
- **OpenWeather API**: Real-time air quality data for Indonesian cities/regencies
- **Local CSV**: Coordinates of 500++ cities/regencies in Indonesia

### Air Quality Parameters Tracked
- AQI (Air Quality Index)
- CO (Carbon Monoxide)
- NO₂ (Nitrogen Dioxide)
- O₃ (Ozone)
- SO₂ (Sulfur Dioxide)
- PM2.5 (Fine Particulate Matter)
- PM10 (Coarse Particulate Matter)

### Data Processing
- **Extract**: Fetch data from OpenWeather API with rate limiting
- **Transform**: Clean data, normalize timestamps to WIB (UTC+7), classify region types (Kota/Kabupaten)
- **Load**: Store processed data in PostgreSQL

## Dashboard Visualization

The processed snapshot data from PostgreSQL (representing the latest air quality state per region) is integrated into a Power BI Dashboard for geographical and criteria-based analysis.

### Key Interactive Features:
- **Dynamic Pollutant Slicer**: Instantly switch visual graphs between `PM2.5`, `PM10`, `NO₂`, `SO₂`, and `O₃` metrics.
- **Top 10 Most Polluted Regions**: Dynamically filters and displays the highest pollution levels across monitored cities/regencies based on the active slicer selection.
- **Semantic KPI Cards**: Live metrics showing the overall national average status and peak pollution areas with qualitative indicators (e.g., *GOOD*, *Very Poor*).

### Demo Preview

![Indonesia Air Quality Dashboard Demo](assets/dashboard-demo.gif)

## Architecture

```
Extract Phase (extract.py)
├─ Read city/regency coordinates from CSV
├─ Call OpenWeather API with 0.2s rate limiting
├─ Wrap raw data (immutable) with metadata
└─ Return: List[Dict] with {metadata, raw_data}
         ↓
Transform Phase (transform.py)
├─ Validate data structure
├─ Extract AQI components
├─ Clean region names (Kabupaten/Kota)
├─ Normalize Unix timestamps to WIB (Asia/Jakarta)
└─ Return: Pandas DataFrame
         ↓
Load Phase (load.py)
├─ Connect to PostgreSQL
├─ Validate configuration
├─ Insert DataFrame
└─ Dispose database connection
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python |
| **API Client** | Requests |
| **Data Processing** | Pandas |
| **Database** | PostgreSQL + SQLAlchemy |
| **Configuration** | Python-dotenv |
| **Logging** | Python logging |
| **Containerization** | Docker + Docker Compose |
| **Visualization** | Power BI |

## Setup & Installation

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- OpenWeather API key ([free tier available](https://openweathermap.org/api))

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/air-pollution-pipeline.git
cd air-pollution-pipeline
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

```env
# OpenWeather API
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=http://api.openweathermap.org/data/2.5/air_pollution

# Database — these values are used by both the app and the PostgreSQL container
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=air_pollution
```

### 3. Run Pipeline
```bash
docker compose up --build
```

Docker Compose will:
1. Start a PostgreSQL container and wait until it is healthy
2. Build the pipeline image and run it against the database
3. Exit automatically once the pipeline completes

### 4. Verify Data
```bash
docker compose exec db psql -U postgres -d air_pollution
```
```sql
SELECT COUNT(*) FROM daily_air_quality;
SELECT * FROM daily_air_quality LIMIT 5;
```

### 5. Cleanup
```bash
docker compose down        # stop containers, keep data
docker compose down -v     # stop containers and delete all data
```

## Project Structure

```
air-pollution-pipeline/
├── src/
│   ├── main.py                    # Pipeline orchestration
│   ├── extract.py                 # Data extraction from API
│   ├── transform.py               # Data transformation & cleaning
│   └── load.py                    # Data loading to PostgreSQL
├── settings/
│   └── path.py                    # Path configuration
├── data/
│   └── lat_long_kota_kab.csv      # City/regency coordinates dataset
├── .dockerignore                  # Files excluded from Docker image
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules
├── compose.yaml                   # Docker Compose configuration
├── Dockerfile                     # Docker image definition
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

**If you find this helpful, please consider starring ⭐ the repository!**