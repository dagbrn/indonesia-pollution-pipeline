import sys
from pathlib import Path

# add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import logging
from settings.path import ENV_PATH
from extract import run_extraction
from transform import run_transformation
from load import run_load

# logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# load environment variables
try:
    load_dotenv(ENV_PATH)
    logger.info(f"Environment variables loaded from {ENV_PATH}")
except Exception as e:
    logger.error(f"Failed to load environment variables: {e}")
    raise

def main() -> None:

    print("--- PIPELINE ETL DIMULAI ---")
    logger.info("Starting ETL pipeline")
    
    try:
        # 1. run extraction
        logger.info("[1/3] Starting extraction...")
        raw_data = run_extraction()
        
        if not raw_data:
            logger.warning("No data extracted. Pipeline stopping.")
            return
        
        logger.info(f"✓ Extraction complete: {len(raw_data)} records")
        
        # 2. run transformation
        logger.info("[2/3] Starting data transformation...")
        df_hasil = run_transformation(raw_data)
        
        if df_hasil.empty:
            logger.warning("No data transformed. Pipeline stopping.")
            return
        
        logger.info(f"✓ Transformation complete: {len(df_hasil)} records")
        
        # 3. run load
        logger.info("[3/3] Starting load phase...")
        run_load(df_hasil)
        
        logger.info("✓ Load complete!")
        print("--- PIPELINE ETL SELESAI ---")
        logger.info("ETL pipeline completed successfully")
        
    except Exception as e:
        print(f"✕ Pipeline failed with error: {e}")
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    
    main()