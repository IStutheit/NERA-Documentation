from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / 'data'
CONTRACTOR_JSON_FILES_DIR = DATA_DIR / 'Contractor_Index_Files'
TEMP_TRAINING_DIR = DATA_DIR / 'temp_training'
TEMP_TRAINING_PROCESSED_DIR = DATA_DIR / 'temp_training_processed'