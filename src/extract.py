import os
from settings.path import DATA_DIR
import requests
import pandas as pd
import time
import logging
import json
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# load and validate API key and base URL from environment
def _load_api_config() -> tuple[str, str]:
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    base_url = os.getenv('OPENWEATHER_BASE_URL')
    
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY not found in .env file")
    if not base_url:
        raise ValueError("OPENWEATHER_BASE_URL not found in .env file")
    
    return api_key, base_url


def run_extraction(csv_path=DATA_DIR / "lat_long_kota_kab.csv") -> List[Dict[str, Any]]:
    
    logger.info("Starting extraction process...")
    
    # 1. load API key and base URL from environment
    try:
        api_key, base_url = _load_api_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    # 2. read and validate csv file
    try:
        df_cities = pd.read_csv(csv_path)
    except FileNotFoundError:
        logger.error(f"CSV file not found at: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise

    all_extracted_data = []
    
    logger.info(f"Total regions to be processed: {len(df_cities)} cities/regencies.")
    
    # 3. loop through each row in csv
    for index, row in df_cities.iterrows():
        nama_wilayah = row['name']
        lat = row['lat']
        lon = row['long']
        
        # build dynamic url using base url
        url = f"{base_url}?lat={lat}&lon={lon}&appid={api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            
            response.raise_for_status()
            data_api = response.json()
            
            # wrap raw data in a new dictionary to keep it immutable 
            # metadata contains city info, raw_data contains untouched API response
            extracted_item = {
                'metadata': {
                    'nama_kota': nama_wilayah
                },
                'raw_data': data_api
            }
            
            all_extracted_data.append(extracted_item)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error pada wilayah {nama_wilayah}: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error pada wilayah {nama_wilayah}: {e}")
            
        # add rate limit to avoid being blocked by API
        time.sleep(0.2)
        
        # simple progress indicator every 50 regions
        if (index + 1) % 50 == 0:
            logger.info(f"Successfully processed {index + 1}/{len(df_cities)} regions...")

    logger.info(f"Extraction complete. Successfully collected {len(all_extracted_data)} region data.")
    
    return all_extracted_data

