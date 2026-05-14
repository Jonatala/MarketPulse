import yfinance as yf
import pandas as pd
import datetime as dt
from pathlib import Path

# BASE_DIR = Path.cwd()
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX", "ORCL", "INTC"]

# Fetch and clean data
def fetch_data(ticker, period="1y"):
    df = yf.Ticker(ticker).history(period=period)

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    df = df.reset_index()

    df["ticker"] = ticker

    df = df.rename(columns={
        "Date": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"})

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    ).dt.tz_localize(None)

    return df[["timestamp", "ticker", "open", "high", "low", "close", "volume"]]


def fetch_all(tickers, period="1y"):
    return pd.concat(
        [fetch_data(t, period) for t in tickers],
        ignore_index=True
    )

# Save Data to CSV

def  save_to_csv(df, ticker):
    date_tag = dt.datetime.utcnow().strftime("%Y%m%d")

    path = DATA_DIR / ticker / f"{date_tag}.csv"

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    print(f"Saved: {path}")

def main():
    print("Fetching multi stock data")

    all_data = []

    for ticker in TICKERS:

        try:
            print(f"fetching {ticker}...")
            df = fetch_data(ticker)

            save_to_csv(df, ticker)

            all_data.append(df)

        except Exception as e:

            print(f"Failed {ticker}: {e}")

    if all_data:

        full_df = pd.concat(all_data,
                            ignore_index=True)

        print(full_df.head())

if __name__ == "__main__":
    main()



