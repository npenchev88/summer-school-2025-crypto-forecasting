import pandas as pd

# Load the Excel file
file_path = r"C:\Users\Kameliya.Stefanova\OneDrive - INDEAVR\Desktop\ks\ПХД\Summer School\Case\BTC_Historical_Data.xlsx"
df = pd.read_excel(file_path)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Convert price columns to float
df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

# Set date as index (optional, useful for time series)
df.set_index('date', inplace=True)

df['prev_close'] = df['close'].shift(1)
df['high_low'] = df['high'] - df['low']
df['high_prev_close'] = abs(df['high'] - df['prev_close'])
df['low_prev_close'] = abs(df['low'] - df['prev_close'])

df['true_range'] = df[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)
df['true_range_pct'] = (df['true_range'] / df['open']) * 100

periods = [7, 30, 90, 365, 1095, 1825, 3650, 7300, 18250]

for period in periods:
    column_name = f'atr_pct_{period}d'
    df[column_name] = df['true_range_pct'].rolling(window=period).mean()

df = df.sort_values('date', ascending=False)  # For display

# Save to Excel (simple)
df.to_excel("BTC_ATR_results5.xlsx", index=False)


