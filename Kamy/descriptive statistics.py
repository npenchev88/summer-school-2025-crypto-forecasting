!pip install scipy
import pandas as pd

url = "https://github.com/npenchev88/summer-school-2025-crypto-forecasting/raw/refs/heads/main/resources/data/BTC_Historical_Data.xlsx"
df = pd.read_excel(url, engine='openpyxl')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# Daily percentage return
df['Daily Return'] = (df['close'] - df['open']) / df['open'] * 100
import numpy as np

# Drop NaN from first row
returns = df['Daily Return'].dropna()

# Basic stats
average_return = returns.mean()
positive_returns = returns[returns > 0]
negative_returns = returns[returns < 0]

avg_positive = positive_returns.mean()
avg_negative = negative_returns.mean()

freq_positive = len(positive_returns)
freq_negative = len(negative_returns)
total_days = len(returns)

perc_positive = freq_positive / total_days * 100
perc_negative = freq_negative / total_days * 100

# number of zero-return days (if relevant)
zero_returns = returns[returns == 0]
freq_zero = len(zero_returns)
perc_zero = freq_zero / total_days * 100

# Format into a summary DataFrame
return_summary = pd.DataFrame({
    'Category': ['Average Return', 'Average Positive', 'Average Negative', 'Zero Returns'],
    'Average Return': [f"{average_return:.2%}", f"{avg_positive:.2%}", f"{avg_negative:.2%}", '0.00%'],
    'Frequency': ['', freq_positive, freq_negative, freq_zero],
    'Frequency %': ['', f"{perc_positive:.2f}%", f"{perc_negative:.2f}%", f"{perc_zero:.2f}%"],
    'Avg Return': ['', f"{avg_positive:.2%}", f"{avg_negative:.2%}", '0.00%']
})

# 🖨️ Print it cleanly
print("\n=== Return Summary ===")
print(return_summary)
# Define bin edges and labels
bin_edges = [-np.inf, -15, -10, -5, -2, 0, 2, 5, 10, 15, np.inf]
bin_labels = [
    "Less than -15%",
    "-15% to -10%",
    "-10% to -5%",
    "-5% to -2%",
    "-2% to 0%",
    "0% to 2%",
    "2% to 5%",
    "5% to 10%",
    "10% to 15%",
    "Greater than 15%"
]

# Assign bins to returns
df['Bin Interval'] = pd.cut(df['Daily Return'], bins=bin_edges)
df['Bin Label'] = pd.cut(df['Daily Return'], bins=bin_edges, labels=bin_labels)

# Group and calculate stats
grouped = df.groupby('Bin Interval')

# Frequency per bin
bin_counts = grouped.size()

# Probability per bin
probabilities = bin_counts / bin_counts.sum() * 100

# Cumulative percentage
cumulative_percentages = probabilities.cumsum()

# Final table with both interval and label
histogram_table = pd.DataFrame({
    'Bin Interval': bin_counts.index.astype(str),   # e.g., "(-15.0, -10.0]"
    'Bin Label': bin_labels,
    'Frequency': bin_counts.values,
    'Probability (%)': probabilities.round(2).values,
    'Cumulative (%)': cumulative_percentages.round(2).values
})

print(histogram_table)
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew, mode

# Assume df['Daily Return'] exists and is numeric
returns = df['Daily Return'].dropna()

# Core stats
mean = returns.mean()
std_dev = returns.std()
std_err = returns.sem()
median = returns.median()
mode_val = mode(returns, keepdims=False).mode
variance = returns.var()
kurt = kurtosis(returns, fisher=False)  # match Excel
skewness = skew(returns)
minimum = returns.min()
maximum = returns.max()
range_val = maximum - minimum
total_sum = returns.sum()
count = returns.count()

# 🟦 Table 1: Descriptive Statistics (Only core metrics)
descriptive_stats = pd.DataFrame({
    'Metric': [
        'Mean', 'Standard Error', 'Median', 'Mode', 'Standard Deviation', 'Sample Variance',
        'Kurtosis', 'Skewness', 'Range', 'Minimum', 'Maximum', 'Sum', 'Count'
    ],
    'Value': [
        mean, std_err, median, mode_val, std_dev, variance,
        kurt, skewness, range_val, minimum, maximum, total_sum, count
    ]
})

# 🟨 Table 2: Std Dev Bands (separate)
std_band_df = pd.DataFrame({
    'Metric': [
        'Mean + 1σ', 'Mean - 1σ',
        'Mean + 2σ', 'Mean - 2σ',
        'Mean + 3σ', 'Mean - 3σ'
    ],
    'Value': [
        mean + std_dev, mean - std_dev,
        mean + 2*std_dev, mean - 2*std_dev,
        mean + 3*std_dev, mean - 3*std_dev
    ]
})

# 🟥 Table 3: Std Dev Distribution Table
within_1_std = returns[(returns >= mean - std_dev) & (returns <= mean + std_dev)]
within_2_std = returns[(returns >= mean - 2*std_dev) & (returns <= mean + 2*std_dev)]
within_3_std = returns[(returns >= mean - 3*std_dev) & (returns <= mean + 3*std_dev)]

actual_counts = [len(within_1_std), len(within_2_std), len(within_3_std)]
normal_percents = [0.682, 0.954, 0.998]
normal_counts = [round(p * count, 3) for p in normal_percents]
actual_percents = [round((x / count) * 100, 2) for x in actual_counts]
normal_percents_percent = [round(p * 100, 2) for p in normal_percents]

std_dev_comparison = pd.DataFrame({
    'Std Dev': [1, 2, 3],
    'Actual Count': actual_counts,
    'Normal Count': normal_counts,
    'Actual %': actual_percents,
    'Normal %': normal_percents_percent
})

# Print the tables
print("\n=== Descriptive Statistics ===")
print(descriptive_stats)

print("\n=== Standard Deviation Bands ===")
print(std_band_df)

print("\n=== Std Dev Coverage Comparison (Actual vs Normal) ===")
print(std_dev_comparison)

from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate normal distribution with same mean and std
normal_data = np.random.normal(loc=mean, scale=actual_std, size=len(returns))

# Plot
sns.histplot(returns, bins=50, color='blue', label='Actual', stat='density', kde=True)
sns.histplot(normal_data, bins=50, color='red', label='Normal', stat='density', kde=True, alpha=0.5)
plt.legend()
plt.title("Actual vs Normal Distribution of Bitcoin Returns")
plt.show()
# Clean daily return series
returns = df['Daily Return'].dropna()

mean = returns.mean()
std = returns.std()
total_count = len(returns)

# Define ranges for 1σ, 2σ, 3σ
within_1_std = returns[(returns >= mean - std) & (returns <= mean + std)]
within_2_std = returns[(returns >= mean - 2*std) & (returns <= mean + 2*std)]
within_3_std = returns[(returns >= mean - 3*std) & (returns <= mean + 3*std)]

# Actual counts
actual_counts = [len(within_1_std), len(within_2_std), len(within_3_std)]

# Normal expected counts (theoretical under normal dist)
normal_percents = [0.682, 0.954, 0.998]
normal_counts = [round(p * total_count, 3) for p in normal_percents]

# Actual percentages
actual_percents = [round((count / total_count) * 100, 2) for count in actual_counts]
normal_percents_percent = [round(p * 100, 2) for p in normal_percents]

# Format result table
std_dev_comparison = pd.DataFrame({
    'Std Dev': [1, 2, 3],
    'Actual Count': actual_counts,
    'Normal Count': normal_counts,
    'Actual %': actual_percents,
    'Normal %': normal_percents_percent
})

print(std_dev_comparison)
output_path = r"C:\Users\Kameliya.Stefanova\OneDrive - INDEAVR\Desktop\ks\ПХД\Summer School\Case\btc_analysis_output2.xlsx"

with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, sheet_name='Data + Returns', index=False)
    histogram_table.to_excel(writer, sheet_name='Histogram Table', index=False)
    pd.DataFrame({
        'Average Return': [average_return],
        'Avg Positive Return': [avg_positive],
        'Avg Negative Return': [avg_negative],
        'Freq Positive': [freq_positive],
        'Freq Negative': [freq_negative],
        'Perc Positive': [perc_positive],
        'Perc Negative': [perc_negative],
        'Std Dev': [actual_std],
        'Mean + 1 SD': [upper_std],
        'Mean - 1 SD': [lower_std]
    }).to_excel(writer, sheet_name='Summary Stats', index=False)

df = df.sort_values('date', ascending=False)  # For display

print("Saved to:", output_path)
