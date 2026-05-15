import pandas as pd
import xgboost as xgb

from sklearn.metrics import classification_report, accuracy_score

# extract needed features from dataset for model training
def prepare_dataset(df):

    df = df.copy()

    # sort dataset for time split

    df = df.sort_values(["timestamp", "ticker"])

    features = ["returns","sma_5","sma_20","volatility_20","volume_change"]

    df = df.dropna()

    X = df[features]
    y = df["target"]

    return df, X, y

# Split dataset for model training
def time_split(df, X, y, split_ratio=0.8):

    split_index = int(len(df) * split_ratio)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    test_df = df.iloc[split_index:].copy()

    return X_train, X_test, y_train, y_test, test_df

# train xgb model

def train_model(X_train, y_train):

    model = xgb.XGBClassifier(n_estimators=200,
                              max_depth=4,
                              learning_rate=0.05,
                              subsample=0.8,
                              colsample_bytree=0.8,
                              random_state=42,
                              eval_metric="logloss")

    model.fit(X_train, y_train)

    return model

# evaluate model
def evaluate(model, X_test, y_test):

    preds = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, preds))
    print("\nClassification Report:\n")
    print(classification_report(y_test, preds))

    return preds

