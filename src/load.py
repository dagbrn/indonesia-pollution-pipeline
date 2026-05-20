import os
from settings.path import ENV_PATH
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)

def _load_db_config() -> dict:
    
    # load and validate database configuration from environment
    db_config = {
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'DB_NAME': os.getenv('DB_NAME')
    }
    
    # validate all required keys
    missing_keys = [key for key, value in db_config.items() if not value]
    if missing_keys:
        raise ValueError(f"Missing database configuration in .env: {missing_keys}")
    
    return db_config


def run_load(dataframe, table_name="daily_air_quality"):

    logger.info("Memulai proses loading data ke database PostgreSQL...")
    
    # load database configuration from environment
    try:
        db_config = _load_db_config()
    except ValueError as e:
        logger.error(f"Database configuration error: {e}")
        raise
    
    # connection to postgres
    # format: postgresql+psycopg://user:password@host:port/database_name
    connection_string = (
        f"postgresql+psycopg://"
        f"{db_config['USER']}:{db_config['PASSWORD']}"
        f"@{db_config['HOST']}:{db_config['PORT']}"
        f"/{db_config['DB_NAME']}"
    )

    try:
        # create database engine
        engine = create_engine(connection_string)
        
        # insert dataframe into postgres
        dataframe.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        
        logger.info(f"Sukses! {len(dataframe)} baris data polusi berhasil disimpan ke tabel '{table_name}' di PostgreSQL.")
        
    except Exception as e:
        logger.error(f"Terjadi error saat loading data ke PostgreSQL: {e}")
        raise
        
    finally:
        # dispose database connection and close all connections in the pool
        engine.dispose()
        logger.info("Database connection disposed successfully.")
