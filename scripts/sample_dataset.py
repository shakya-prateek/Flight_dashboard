import pandas as pd
import os
import shutil

RAW_PATH = 'data/raw/'
ORIGINAL_FILE = os.path.join(RAW_PATH, 'flights.csv')
BACKUP_FILE = os.path.join(RAW_PATH, 'flights_full.csv.bak')
SAMPLE_SIZE = 100000
SEED = 42

def sample_data():
    if not os.path.exists(ORIGINAL_FILE):
        print(f"Error: {ORIGINAL_FILE} not found.")
        return

    print(f"Backing up {ORIGINAL_FILE} to {BACKUP_FILE}...")
    shutil.copy2(ORIGINAL_FILE, BACKUP_FILE)
    
    print(f"Loading data from {BACKUP_FILE}...")
    # Load the full dataset (it's around 565MB, should be fine)
    df = pd.read_csv(BACKUP_FILE, low_memory=False)
    
    print(f"Total rows in original: {len(df):,}")
    
    if len(df) <= SAMPLE_SIZE:
        print("Dataset is already smaller than or equal to 100k rows. No sampling needed.")
        return
    
    print(f"Sampling {SAMPLE_SIZE:,} rows...")
    df_sample = df.sample(n=SAMPLE_SIZE, random_state=SEED)
    
    print(f"Saving sample to {ORIGINAL_FILE}...")
    df_sample.to_csv(ORIGINAL_FILE, index=False)
    
    print(f"SUCCESS: Sampled dataset saved with {len(df_sample):,} rows.")

if __name__ == "__main__":
    sample_data()
