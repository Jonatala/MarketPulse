from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

def load_ticker(ticker: str)-> pd.DataFrame:

    ticker_path = RAW_DIR / ticker

    print("Ticker path:", ticker_path)

    files = sorted(ticker_path.glob("*.csv"))

    dfs = []

    for file in files:

        df = pd.read_csv(file)

        print("Files found:", files)

        # parse timestamp column
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # clean dataset

    df = df.dropna()

    df = (df.sort_values(["ticker","timestamp"]).drop_duplicates().reset_index(drop=True))

    return df

def load_all(tickers: list[str])-> pd.DataFrame:

    dfs = []

    for ticker in tickers:

        df = load_ticker(ticker)

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
