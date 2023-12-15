import csv
import pandas as pd
import numpy as np

# Open original CSV
# IMPORT the CSV file to the Colab first
filepath = r"MySlate_9_iPhone.csv"
df = pd.read_csv(filepath)

# Filter data
window = 90
col_names = list(df.columns)
for i in range(1, len(col_names)):
  c = col_names[i]
  df[c] = df[c].rolling(window).mean()

df.dropna(inplace=True)

# Save filtered CSV and DOWNLOAD it
save_file = 'filtered{}_'.format(window) + filepath
df.to_csv(save_file, index=False)