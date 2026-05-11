import yfinance as yf
import pandas as pd
import datetime as dt
import os

DATA_DIR = "../../data/raw"
FILE_PATH = os.path.join(DATA_DIR, )

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "^GSPC", "TSLA", "^VIX"]

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


def fetch_all(tickers, period="1yr"):
    return pd.concat(
        [fetch_data(t, period) for t in tickers],
        ignore_index=True
    )

# Save Data to CSV

def  save_to_csv(df, ticker):
    date_tag = dt.datetime.utcnow().strftime("%Y%m%d")

    path = f"../../data/raw/{ticker}/{date_tag}.csv"

    os.makedirs(os.path.dirname(path), exist_ok=True)

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

        full_df = pd.concat(all_data)

        print(full_df.head())

if __name__ == "__main__":
    main()



