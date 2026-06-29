import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path, encoding="latin1")
    return df

def clean_data(df):
    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Order ID","Order Date","Customer ID","Segment","Region","Category","Sub-Category","Product Name","Sales"])
    df = df[df["Sales"] > 0]
    df["Ship Delay"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["YearMonth"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df