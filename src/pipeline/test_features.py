from src.data_access.load_data import (load_ticker, load_all)
from src.features.build_features import (
    build_features, create_target, save_processed)

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "^GSPC", "TSLA", "^VIX"]

# choose ticker
#ticker = "AAPL"

#df = load_ticker(ticker)

df = load_all(TICKERS)

# Load raw data
print("Raw data loaded:")
print(df.head(2))

# Build features
df_features = build_features(df)

# Create target
df_features = create_target(df_features)
print(df_features.head(2))

print("Feature dataframe:")
print(df_features.head(2))

save_processed(df_features,"ALL_TICKERS")

print("Feature pipeline completed")