import sqlite3
import json
import os

DB_FILE = "weather.db"
JSON_FILE = "weather_data.json"

def create_tables(cursor):
    """Creates the necessary tables if they don't exist."""
    print("Creating tables...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        weather_desc TEXT,
        weather_id TEXT,
        max_temp INTEGER,
        min_temp INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (region_id) REFERENCES regions (id)
    )
    """)

def import_data(cursor, data):
    """Imports data from the parsed JSON object."""
    print("Importing data...")
    
    try:
        # Navigate to the relevant data
        locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    except KeyError as e:
        print(f"Error parsing JSON structure: {e}")
        return

    for loc in locations:
        region_name = loc['locationName']
        
        # Insert region or get existing ID
        cursor.execute("SELECT id FROM regions WHERE name = ?", (region_name,))
        result = cursor.fetchone()
        
        if result:
            region_id = result[0]
        else:
            cursor.execute("INSERT INTO regions (name) VALUES (?)", (region_name,))
            region_id = cursor.lastrowid
            print(f"Added region: {region_name}")

        # Process weather elements
        weather_elements = loc['weatherElements']
        
        # Helper to organize data by date
        # structure: { "YYYY-MM-DD": { "Wx": ..., "MaxT": ..., "MinT": ... } }
        daily_data = {}

        # Process Wx
        if 'Wx' in weather_elements and 'daily' in weather_elements['Wx']:
            for item in weather_elements['Wx']['daily']:
                date = item['dataDate']
                if date not in daily_data: daily_data[date] = {}
                daily_data[date]['weather_desc'] = item['weather']
                daily_data[date]['weather_id'] = item['weatherid']

        # Process MaxT
        if 'MaxT' in weather_elements and 'daily' in weather_elements['MaxT']:
            for item in weather_elements['MaxT']['daily']:
                date = item['dataDate']
                if date not in daily_data: daily_data[date] = {}
                daily_data[date]['max_temp'] = int(item['temperature'])

        # Process MinT
        if 'MinT' in weather_elements and 'daily' in weather_elements['MinT']:
            for item in weather_elements['MinT']['daily']:
                date = item['dataDate']
                if date not in daily_data: daily_data[date] = {}
                daily_data[date]['min_temp'] = int(item['temperature'])
        
        # Insert into forecasts
        for date, info in daily_data.items():
            # Check for existing record to avoid duplicates (optional, based on requirement, here we just insert)
            # A simple duplicate check: DELETE existing for this region/date before insert, or just INSERT
            # For this task, simple INSERT is fine as requirement didn't specify upsert logic, 
            # but let's clear old data for this region/date to be safe if running multiple times? 
            # Or just ignore constraints. Let's stick to simple INSERT.
            
            cursor.execute("""
            INSERT INTO forecasts (region_id, date, weather_desc, weather_id, max_temp, min_temp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                region_id,
                date,
                info.get('weather_desc'),
                info.get('weather_id'),
                info.get('max_temp'),
                info.get('min_temp')
            ))
        print(f"Imported forecasts for {region_name}")

def main():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        create_tables(cursor)
        import_data(cursor, data)
        conn.commit()
        print("Data import completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
