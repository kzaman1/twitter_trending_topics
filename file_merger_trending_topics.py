import os
import glob
import re
import pandas as pd

# Path to the folder containing the CSVs
folder_path = '/path/to/folder'

# Get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
print(csv_files)

# Combine all CSVs into a single DataFrame
df = pd.concat([pd.read_csv(f, skiprows=1, header=None) for f in csv_files])
print(df)

# Drop the 1st column which is the old index
df = df.drop(columns=df.columns[0])

# Add the column headers
df.columns = ['date_scraped', 'rank', 'trending_topic', 'tweet_volume', 'url']
print(df)

# Sort by the date_scraped column from oldest to newest
df = df.sort_values(by=['date_scraped', 'rank'], ascending=[True, True])

# Reset the index
df = df.reset_index(drop=True)

# Export the combined CSV
output_filename = f"{folder_path}\\combined_trending_topics.csv"
df.to_csv(output_filename, index=False)
