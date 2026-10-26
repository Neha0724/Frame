from pathlib import Path
import os
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'
CLEAN_DATA_PATH = ROOT_DIR / 'output' / 'anime_clean'
RAW_DATA_PATH = DATA_DIR / 'anime.csv'
MODEL_PATH = ROOT_DIR / 'models' / 'anime_rating_model.pkl'
PORT = int(os.getenv('PORT', '5000'))
