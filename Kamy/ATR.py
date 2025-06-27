import pandas as pd

url = "https://github.com/npenchev88/summer-school-2025-crypto-forecasting/raw/refs/heads/main/resources/data/BTC_Historical_Data.xlsx"
df = pd.read_excel(url, engine='openpyxl')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

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
df.to_excel("BTC_ATR_results.xlsx", index=False)


