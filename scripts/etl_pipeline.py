"""
ETL Pipeline — US Flight Delays 2015
=====================================
Consolidated script for the complete Extract-Transform-Load pipeline.
Reads raw CSV files from data/raw/, cleans and transforms them, and exports
cleaned datasets to data/processed/.

Usage:
    python scripts/etl_pipeline.py

Author: DVA Capstone 2 Team
"""

import pandas as pd
import numpy as np
import os
import sys
import time


# ============================================================================
# CONFIGURATION
# ============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')
TABLEAU_DATA_PATH = os.path.join(PROCESSED_DATA_PATH, 'tableau')


def log(message):
    """Simple logging with timestamp."""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")


# ============================================================================
# STEP 1: EXTRACT — Load raw data
# ============================================================================
def extract():
    """Load all raw CSV files."""
    log("=" * 60)
    log("STEP 1: EXTRACTION")
    log("=" * 60)

    log("Loading airlines.csv...")
    df_airlines = pd.read_csv(os.path.join(RAW_DATA_PATH, 'airlines.csv'))
    log(f"  Airlines: {df_airlines.shape}")

    log("Loading airports.csv...")
    df_airports = pd.read_csv(os.path.join(RAW_DATA_PATH, 'airports.csv'))
    log(f"  Airports: {df_airports.shape}")

    log("Loading flights.csv (this may take a moment)...")
    df_flights = pd.read_csv(os.path.join(RAW_DATA_PATH, 'flights.csv'), low_memory=False)
    log(f"  Flights: {df_flights.shape}")

    return df_airlines, df_airports, df_flights


# ============================================================================
# STEP 2: TRANSFORM — Clean and engineer features
# ============================================================================
def transform(df_airlines, df_airports, df_flights):
    """Clean data, handle missing values, engineer features, merge references."""
    log("=" * 60)
    log("STEP 2: TRANSFORMATION")
    log("=" * 60)

    initial_shape = df_flights.shape
    log(f"Initial shape: {initial_shape}")

    # --- 2a: Handle missing values ---
    log("Handling missing values...")

    # Fill delay breakdown columns with 0
    delay_columns = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
                     'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    for col in delay_columns:
        df_flights[col] = df_flights[col].fillna(0)

    # Fill cancellation reason
    df_flights['CANCELLATION_REASON'] = df_flights['CANCELLATION_REASON'].fillna('N')
    cancellation_map = {
        'A': 'Airline/Carrier', 'B': 'Weather',
        'C': 'National Air System', 'D': 'Security', 'N': 'Not Cancelled'
    }
    df_flights['CANCELLATION_REASON_DESC'] = df_flights['CANCELLATION_REASON'].map(cancellation_map)

    # Fill tail number
    df_flights['TAIL_NUMBER'] = df_flights['TAIL_NUMBER'].fillna('UNKNOWN')
    log("  ✅ Missing values handled.")

    # --- 2b: Create DATE column ---
    log("Creating DATE column...")
    df_flights['DATE'] = pd.to_datetime(
        df_flights[['YEAR', 'MONTH', 'DAY']].assign(
            YEAR=df_flights['YEAR'].astype(str),
            MONTH=df_flights['MONTH'].astype(str).str.zfill(2),
            DAY=df_flights['DAY'].astype(str).str.zfill(2)
        ).agg('-'.join, axis=1),
        format='%Y-%m-%d', errors='coerce'
    )
    log(f"  Date range: {df_flights['DATE'].min()} to {df_flights['DATE'].max()}")

    # --- 2c: Convert time columns ---
    log("Converting time columns...")

    def convert_hhmm(val):
        if pd.isna(val):
            return np.nan
        val = int(val)
        if val == 2400:
            val = 0
        hours = val // 100
        minutes = val % 100
        return f"{hours:02d}:{minutes:02d}"

    for col in ['SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL']:
        df_flights[col + '_TIME'] = df_flights[col].apply(convert_hhmm)

    # --- 2d: Time-based features ---
    log("Engineering time-based features...")
    month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df_flights['MONTH_NAME'] = df_flights['MONTH'].map(month_map)

    day_map = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
               5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    df_flights['DAY_NAME'] = df_flights['DAY_OF_WEEK'].map(day_map)

    df_flights['QUARTER'] = df_flights['MONTH'].apply(lambda x: f"Q{(x - 1) // 3 + 1}")
    df_flights['DEP_HOUR'] = (df_flights['SCHEDULED_DEPARTURE'] // 100).astype('Int64')

    def get_time_of_day(hour):
        if pd.isna(hour):
            return 'Unknown'
        hour = int(hour)
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    df_flights['TIME_OF_DAY'] = df_flights['DEP_HOUR'].apply(get_time_of_day)
    log("  ✅ Time features created.")

    # --- 2e: Outlier flags ---
    log("Flagging outliers...")
    df_flights['IS_EXTREME_DEP_DELAY'] = (df_flights['DEPARTURE_DELAY'] > 180).astype(int)
    df_flights['IS_EXTREME_ARR_DELAY'] = (df_flights['ARRIVAL_DELAY'] > 180).astype(int)

    for col in ['DEPARTURE_DELAY', 'ARRIVAL_DELAY']:
        cap_val = df_flights[col].quantile(0.995)
        df_flights[col + '_CAPPED'] = df_flights[col].clip(upper=cap_val)

    # --- 2f: Delay classification ---
    log("Classifying delays...")

    def classify_delay(delay):
        if pd.isna(delay):
            return 'Cancelled'
        elif delay <= 0:
            return 'On Time / Early'
        elif delay <= 15:
            return 'Minor Delay (1-15 min)'
        elif delay <= 60:
            return 'Moderate Delay (16-60 min)'
        elif delay <= 180:
            return 'Significant Delay (1-3 hrs)'
        else:
            return 'Severe Delay (3+ hrs)'

    df_flights['DELAY_CATEGORY'] = df_flights['ARRIVAL_DELAY'].apply(classify_delay)
    df_flights['IS_DELAYED'] = (df_flights['ARRIVAL_DELAY'] > 15).astype('Int64')
    df_flights.loc[df_flights['ARRIVAL_DELAY'].isna(), 'IS_DELAYED'] = pd.NA

    # --- 2g: Delay cause analysis ---
    log("Analyzing delay causes...")
    df_flights['TOTAL_DELAY_BREAKDOWN'] = (
        df_flights['AIR_SYSTEM_DELAY'] + df_flights['SECURITY_DELAY'] +
        df_flights['AIRLINE_DELAY'] + df_flights['LATE_AIRCRAFT_DELAY'] +
        df_flights['WEATHER_DELAY']
    )

    delay_type_cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
                       'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    df_flights['PRIMARY_DELAY_CAUSE'] = df_flights[delay_type_cols].idxmax(axis=1)
    df_flights.loc[df_flights['TOTAL_DELAY_BREAKDOWN'] == 0, 'PRIMARY_DELAY_CAUSE'] = 'No Delay'

    cause_rename = {
        'AIR_SYSTEM_DELAY': 'Air System', 'SECURITY_DELAY': 'Security',
        'AIRLINE_DELAY': 'Airline/Carrier', 'LATE_AIRCRAFT_DELAY': 'Late Aircraft',
        'WEATHER_DELAY': 'Weather', 'No Delay': 'No Delay'
    }
    df_flights['PRIMARY_DELAY_CAUSE'] = df_flights['PRIMARY_DELAY_CAUSE'].map(cause_rename)

    # --- 2h: Distance categories ---
    def classify_distance(dist):
        if pd.isna(dist):
            return 'Unknown'
        elif dist <= 500:
            return 'Short-haul (≤500 mi)'
        elif dist <= 1500:
            return 'Medium-haul (501-1500 mi)'
        else:
            return 'Long-haul (>1500 mi)'

    df_flights['DISTANCE_CATEGORY'] = df_flights['DISTANCE'].apply(classify_distance)

    # --- 2i: Route column ---
    df_flights['ROUTE'] = (df_flights['ORIGIN_AIRPORT'].astype(str) + ' → ' +
                           df_flights['DESTINATION_AIRPORT'].astype(str))

    # --- 2j: Merge reference tables ---
    log("Merging reference tables...")
    df_flights = df_flights.merge(
        df_airlines.rename(columns={'IATA_CODE': 'AIRLINE', 'AIRLINE': 'AIRLINE_NAME'}),
        on='AIRLINE', how='left'
    )

    origin_cols = df_airports.rename(columns={
        'IATA_CODE': 'ORIGIN_AIRPORT', 'AIRPORT': 'ORIGIN_AIRPORT_NAME',
        'CITY': 'ORIGIN_CITY', 'STATE': 'ORIGIN_STATE',
        'LATITUDE': 'ORIGIN_LAT', 'LONGITUDE': 'ORIGIN_LONG'
    })[['ORIGIN_AIRPORT', 'ORIGIN_AIRPORT_NAME', 'ORIGIN_CITY',
        'ORIGIN_STATE', 'ORIGIN_LAT', 'ORIGIN_LONG']]
    df_flights = df_flights.merge(origin_cols, on='ORIGIN_AIRPORT', how='left')

    dest_cols = df_airports.rename(columns={
        'IATA_CODE': 'DESTINATION_AIRPORT', 'AIRPORT': 'DEST_AIRPORT_NAME',
        'CITY': 'DEST_CITY', 'STATE': 'DEST_STATE',
        'LATITUDE': 'DEST_LAT', 'LONGITUDE': 'DEST_LONG'
    })[['DESTINATION_AIRPORT', 'DEST_AIRPORT_NAME', 'DEST_CITY',
        'DEST_STATE', 'DEST_LAT', 'DEST_LONG']]
    df_flights = df_flights.merge(dest_cols, on='DESTINATION_AIRPORT', how='left')

    log(f"  ✅ Transformation complete. Final shape: {df_flights.shape}")
    log(f"  New columns added: {df_flights.shape[1] - initial_shape[1]}")

    # Validation
    assert len(df_flights) == initial_shape[0], "Row count mismatch — data loss detected!"
    log("  ✅ Validation passed — no data loss.")

    return df_flights, df_airlines, df_airports


# ============================================================================
# STEP 3: LOAD — Export cleaned data
# ============================================================================
def load(df_flights, df_airlines, df_airports):
    """Export cleaned datasets to processed directory."""
    log("=" * 60)
    log("STEP 3: LOAD")
    log("=" * 60)

    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    os.makedirs(TABLEAU_DATA_PATH, exist_ok=True)

    # Save main cleaned dataset
    output_path = os.path.join(PROCESSED_DATA_PATH, 'flights_cleaned.csv')
    log(f"Saving cleaned flights → {output_path}")
    df_flights.to_csv(output_path, index=False)
    log(f"  Size: {os.path.getsize(output_path) / (1024 ** 2):.2f} MB")

    # Save reference tables
    df_airlines.to_csv(os.path.join(PROCESSED_DATA_PATH, 'airlines_cleaned.csv'), index=False)
    df_airports.to_csv(os.path.join(PROCESSED_DATA_PATH, 'airports_cleaned.csv'), index=False)
    log("  ✅ Reference tables saved.")

    log("  ✅ Load complete.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Run the full ETL pipeline."""
    start_time = time.time()

    log("=" * 60)
    log("US FLIGHT DELAYS 2015 — ETL PIPELINE")
    log("=" * 60)

    # Step 1: Extract
    df_airlines, df_airports, df_flights = extract()

    # Step 2: Transform
    df_flights, df_airlines, df_airports = transform(df_airlines, df_airports, df_flights)

    # Step 3: Load
    load(df_flights, df_airlines, df_airports)

    elapsed = time.time() - start_time
    log("=" * 60)
    log(f"PIPELINE COMPLETE — Total time: {elapsed:.1f} seconds")
    log("=" * 60)


if __name__ == '__main__':
    main()
