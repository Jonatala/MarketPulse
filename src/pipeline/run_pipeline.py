import pandas as pd
from pathlib import Path

from src.data_access import load_ticker
from src.features.build_features import build_features

RAW_DIR = path("../../data/raw")
PROCESSED_DIR =path("../../data/processed")



