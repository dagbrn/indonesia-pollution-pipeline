import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def run_transformation(data) -> pd.DataFrame:
    logger.info("Start transforming data...")
    
    cleaned_rows = []
    failed_count = 0
    
    for index, item in enumerate(data):
        try:
            # extract metadata and raw API data (keeping raw data immutable)
            if 'metadata' not in item or 'raw_data' not in item:
                logger.warning(f"Row {index}: Missing 'metadata' or 'raw_data' field")
                failed_count += 1
                continue
            
            metadata = item['metadata']
            raw_data = item['raw_data']
            
            # extract city name from metadata
            if 'nama_kota' not in metadata:
                logger.warning(f"Row {index}: Missing 'nama_kota' in metadata")
                failed_count += 1
                continue
            
            raw_name = metadata['nama_kota']
            
            # validate raw_data structure
            if 'list' not in raw_data or not isinstance(raw_data['list'], list) or not raw_data['list']:
                logger.warning(f"Row {index} ({raw_name}): Missing or empty 'list' in raw_data")
                failed_count += 1
                continue
            
            data_list = raw_data['list'][0]
            
            # validate required fields
            if 'main' not in data_list or 'aqi' not in data_list['main']:
                logger.warning(f"Row {index} ({raw_name}): Missing 'main.aqi' in data")
                failed_count += 1
                continue
            
            if 'components' not in data_list:
                logger.warning(f"Row {index} ({raw_name}): Missing 'components' in data")
                failed_count += 1
                continue
            
            # extract main data
            aqi_value = data_list['main']['aqi']
            components = data_list['components']
            unix_timestamp = data_list['dt']
            
            # determine region type
            if "KABUPATEN " in raw_name:
                jenis_wilayah = "Kabupaten"
                cleaned_name = raw_name.replace("KABUPATEN ", "").title()
            elif "KOTA" in raw_name:
                jenis_wilayah = "Kota"
                cleaned_name = raw_name.replace("KOTA ", "").title()
            else:
                jenis_wilayah = "Lainnya"
                cleaned_name = raw_name.title()
            
            # transform unix time to local format (YYYY-MM-DD HH:MM:SS)
            readable_time = datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            # merge into one flat data structure
            row = {
                "jenis_wilayah": jenis_wilayah,
                "nama_kota": cleaned_name,
                "waktu_catat": readable_time,
                "indeks_aqi": aqi_value,
                "co": components['co'],
                "no2": components['no2'],
                "o3": components['o3'],
                "so2": components['so2'],
                "pm2_5": components['pm2_5'],
                "pm10": components['pm10']
            }
            
            cleaned_rows.append(row)
            
        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Row {index}: Error extracting/transforming data: {e}")
            failed_count += 1
            continue
        except Exception as e:
            logger.error(f"Row {index}: Unexpected error: {e}")
            failed_count += 1
            continue
    
    # merge all list of dictionary into one dataframe
    if cleaned_rows:
        final_df = pd.DataFrame(cleaned_rows)
        logger.info(f"Transformasi selesai! Berhasil: {len(cleaned_rows)}, Gagal: {failed_count}")
    else:
        logger.warning(f"No rows were successfully transformed. Failed: {failed_count}")
        final_df = pd.DataFrame()
    
    return final_df