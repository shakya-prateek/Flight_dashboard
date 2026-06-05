import pandas as pd
import numpy as np
import os

PROCESSED_PATH = 'data/processed/'
TABLEAU_PATH = 'data/processed/tableau/'
os.makedirs(TABLEAU_PATH, exist_ok=True)

def prepare_tableau_data():
    print(f"Loading cleaned data from {PROCESSED_PATH}flights_cleaned.csv...")
    df = pd.read_csv(os.path.join(PROCESSED_PATH, 'flights_cleaned.csv'), low_memory=False)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df_nc = df[df['CANCELLED'] == 0].copy()

    # 1. Airline Summary
    print("Generating airline summary...")
    airline_summary = df.groupby(['AIRLINE', 'AIRLINE_NAME']).agg(
        total_flights=('FLIGHT_NUMBER', 'count'),
        cancelled_flights=('CANCELLED', 'sum'),
        avg_departure_delay=('DEPARTURE_DELAY', 'mean'),
        avg_arrival_delay=('ARRIVAL_DELAY', 'mean')
    ).reset_index()
    airline_summary.to_csv(os.path.join(TABLEAU_PATH, 'tableau_airline_summary.csv'), index=False)

    # 2. Airport Summary
    print("Generating airport summary...")
    airport_summary = df_nc.groupby(['ORIGIN_AIRPORT', 'ORIGIN_AIRPORT_NAME', 'ORIGIN_CITY', 'ORIGIN_STATE', 'ORIGIN_LAT', 'ORIGIN_LONG']).agg(
        total_departures=('FLIGHT_NUMBER', 'count'),
        avg_dep_delay=('DEPARTURE_DELAY', 'mean'),
        avg_arr_delay=('ARRIVAL_DELAY', 'mean')
    ).reset_index()
    airport_summary.to_csv(os.path.join(TABLEAU_PATH, 'tableau_airport_summary.csv'), index=False)

    # 3. Monthly Trends
    print("Generating monthly trends...")
    monthly_trends = df.groupby(['MONTH', 'MONTH_NAME']).agg(
        total_flights=('FLIGHT_NUMBER', 'count'),
        avg_arrival_delay=('ARRIVAL_DELAY', 'mean')
    ).reset_index()
    monthly_trends.to_csv(os.path.join(TABLEAU_PATH, 'tableau_monthly_trends.csv'), index=False)

    # 4. Route Analysis
    print("Generating route analysis...")
    route_analysis = df_nc.groupby(['ROUTE', 'ORIGIN_CITY', 'DEST_CITY']).agg(
        flight_count=('FLIGHT_NUMBER', 'count'),
        avg_arr_delay=('ARRIVAL_DELAY', 'mean')
    ).reset_index().nlargest(200, 'flight_count')
    route_analysis.to_csv(os.path.join(TABLEAU_PATH, 'tableau_route_analysis.csv'), index=False)

    # 5. Delay Causes
    print("Generating delay causes...")
    delay_causes = df_nc.groupby(['AIRLINE_NAME', 'MONTH_NAME']).agg(
        avg_air_system_delay=('AIR_SYSTEM_DELAY', 'mean'),
        avg_security_delay=('SECURITY_DELAY', 'mean'),
        avg_airline_delay=('AIRLINE_DELAY', 'mean'),
        avg_late_aircraft_delay=('LATE_AIRCRAFT_DELAY', 'mean'),
        avg_weather_delay=('WEATHER_DELAY', 'mean')
    ).reset_index()
    delay_causes.to_csv(os.path.join(TABLEAU_PATH, 'tableau_delay_causes.csv'), index=False)

    # 6. Hourly Patterns
    print("Generating hourly patterns...")
    hourly_pattern = df_nc.groupby(['DAY_NAME', 'DEP_HOUR']).agg(
        flight_count=('FLIGHT_NUMBER', 'count'),
        avg_arr_delay=('ARRIVAL_DELAY', 'mean')
    ).reset_index()
    hourly_pattern.to_csv(os.path.join(TABLEAU_PATH, 'tableau_hourly_pattern.csv'), index=False)

    # 7. Flight Sample (10% of the 100k = 10k)
    print("Generating flight sample...")
    df_sample = df.sample(frac=0.1, random_state=42)
    df_sample.to_csv(os.path.join(TABLEAU_PATH, 'tableau_flights_sample.csv'), index=False)

    print(f"SUCCESS: All Tableau datasets exported to {TABLEAU_PATH}")

if __name__ == "__main__":
    prepare_tableau_data()
