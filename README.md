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
- **Transform**: Clean data, normalize timestamps, classify region types (Kota/Kabupaten)
- **Load**: Store processed data in PostgreSQL

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
├─ Normalize Unix timestamps
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

## Setup & Installation

### Prerequisites
- Python 3+
- PostgreSQL database
- OpenWeather API key (free tier available)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/air-pollution-pipeline.git
cd air-pollution-pipeline
```

### 2. Create Virtual Environment
```bash
python -m venv venv
On Linux / macOS: 'source venv/bin/activate'  # On Windows: 'venv\Scripts\activate'
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

Then edit `.env` with your configuration:
```env
# OpenWeather API Configuration
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=http://api.openweathermap.org/data/2.5/air_pollution

# Database Configuration
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_NAME=air_pollution
DB_PORT=5432
```

### 5. Create PostgreSQL Database
Create the database using PostgreSQL `createdb` utility:
```bash
createdb -U postgres air_pollution
```

Or using `psql`:
```bash
psql -U postgres -c "CREATE DATABASE air_pollution;"
```

### 6. Run Pipeline
```bash
python src/main.py
```

## 📁 Project Structure

```
air-pollution-pipeline/
├── src/
│   ├── main.py           # Main orchestration
│   ├── extract.py        # Data extraction from API
│   ├── transform.py      # Data transformation & cleaning
│   └── load.py          # Data loading to PostgreSQL
├── settings/
│   └── path.py          # Path configuration
├── data/
│   └── lat_long_kota_kab.csv  # City/Regency coordinates dataset
├── .env                 # Environment variables
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

**⭐ If you find this helpful, please consider starring the repository!**
