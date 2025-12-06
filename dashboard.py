
import streamlit as st
import sqlite3
import pandas as pd
import datetime

# Database Connection
DB_FILE = "weather.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def load_data():
    conn = get_connection()
    query = """
    SELECT 
        f.date,
        r.name as region,
        f.weather_desc,
        f.max_temp,
        f.min_temp
    FROM forecasts f
    JOIN regions r ON f.region_id = r.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Coordinate Mapping
REGION_COORDS = {
    "北部地區": {"lat": 24.9, "lon": 121.5},
    "中部地區": {"lat": 24.1, "lon": 120.6},
    "南部地區": {"lat": 23.0, "lon": 120.3},
    "東北部地區": {"lat": 24.6, "lon": 121.7},
    "東部地區": {"lat": 23.9, "lon": 121.5},
    "東南部地區": {"lat": 22.7, "lon": 121.0}
}

# Page Configuration
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Sidebar
st.sidebar.header("溫度分布圖")
st.sidebar.write("## 篩選條件")

# Load Data
df = load_data()

if df.empty:
    st.error("No data found in database. Please run init_db.py first.")
    st.stop()

# Date Selection
dates = sorted(df['date'].unique())
selected_date = st.sidebar.selectbox("選擇日期", dates)

# Display Options
show_data = st.sidebar.checkbox("顯示詳細資料表", value=False)
show_values = st.sidebar.checkbox("在地圖上顯示數值", value=True)

# Filter Data
daily_df = df[df['date'] == selected_date].copy()

# Add coordinates
daily_df['lat'] = daily_df['region'].map(lambda x: REGION_COORDS.get(x, {}).get('lat'))
daily_df['lon'] = daily_df['region'].map(lambda x: REGION_COORDS.get(x, {}).get('lon'))

# Main Content
st.title(f"溫度分布圖 - {selected_date}")

# Metrics Row
cols = st.columns(len(daily_df))
for idx, row in enumerate(daily_df.itertuples()):
    with cols[idx % 3]: # Wrap around if too many regions for one row, or just list them
        st.metric(
            label=row.region,
            value=f"{row.min_temp}°C - {row.max_temp}°C",
            delta=row.weather_desc
        )

st.divider()

# Map Visualization
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("台灣氣溫分佈")
    # Basic map with points
    # For a more advanced map referencing the image (color coding etc), we'd need pydeck or folium
    # But st.map is simple and matches the request for "reference presentation" logic roughly.
    # To color code by temperature, st.map is limited (it's just dots).
    # Let's use st.map for now as per plan.
    st.map(daily_df[['lat', 'lon']], zoom=7)

with col2:
    st.subheader("地區資訊")
    for _, row in daily_df.iterrows():
        st.write(f"**{row['region']}**")
        st.write(f"氣溫: {row['min_temp']} ~ {row['max_temp']} °C")
        st.write(f"天氣: {row['weather_desc']}")
        st.write("---")

if show_data:
    st.subheader("詳細資料")
    st.dataframe(daily_df)
