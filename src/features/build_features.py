import pandas as pd
from pathlib import Path
import datetime as dt

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def build_features(df):

    df = df.copy()

    # Sort chronologically

    df = df.sort_values(["ticker","timestamp"])

    grouped = df.groupby("ticker")

    # Daily returns
    df["returns"] = grouped["close"].pct_change(fill_method=None)

    # Moving averages
    df["sma_5"] = grouped["close"].transform(lambda x: x.rolling(5).mean())
    df["sma_20"] = grouped["close"].transform(lambda x: x.rolling(20).mean())

    # Volatility
    df["volatility_20"] = (grouped["returns"]
                           .transform(lambda x: x.rolling(20).std()))

    #Volume momentum
    df["volume_change"] = (grouped["volume"].pct_change(fill_method=None))

    # Remove rows with NaNs
    df = df.dropna().reset_index(drop=True)

    return df

# Create target
def create_target(df):
    df.copy()

    df["target"] = (
            df.groupby("ticker")["close"]
            .shift(-1) > df["close"]
    )

    df["target"] = df["target"].astype(int)

    return df

# SAVE PROCESSED DATA
def save_processed(df, ticker):

    # Create date versioning
    date_tag = dt.datetime.utcnow().strftime("%Y%m%d")

    # build output path
    output_dir = PROCESSED_DIR / ticker
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{date_tag}_features.csv"

    # save dataframe
    df.to_csv(output_path, index=False)

    print((f"Saved processed features: {output_path}"))









