
import streamlit as st
import sqlite3
import pandas as pd
import pydeck as pdk
from geojson_map_data import load_and_process_geojson

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
        f.weather_id,
        f.max_temp,
        f.min_temp
    FROM forecasts f
    JOIN regions r ON f.region_id = r.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Color Logic
def get_color(temp):
    # Map temp 15-35 to color
    # Cool (Blue) -> Hot (Red)
    min_t, max_t = 15, 30
    t = max(min_t, min(max_t, temp))
    ratio = (t - min_t) / (max_t - min_t)
    r = int(255 * ratio)
    b = int(255 * (1 - ratio))
    # Alpha 180 for solid look
    return [r, 0, b, 180]

# Page Config
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

# Data for selected date
daily_df = df[df['date'] == selected_date].copy()

# Prepare GeoJSON Data
# We need to inject the color and info into the GeoJSON properties for PyDeck to read
geojson_data = load_and_process_geojson()
# Convert daily_df to a dict for fast lookup: region -> {avg_temp, desc}
region_info = {}
for _, row in daily_df.iterrows():
    avg_temp = (row['min_temp'] + row['max_temp']) / 2
    region_info[row['region']] = {
        "color": get_color(avg_temp),
        "info": f"{row['region']}\n{row['min_temp']}~{row['max_temp']}°C\n{row['weather_desc']}"
    }

# Update GeoJSON properties
for feature in geojson_data["features"]:
    region = feature["properties"].get("region")
    if region and region in region_info:
        feature["properties"]["fill_color"] = region_info[region]["color"]
        feature["properties"]["tooltip_info"] = region_info[region]["info"]
    else:
        # Default grey for unmapped or no data
        feature["properties"]["fill_color"] = [200, 200, 200, 100]
        feature["properties"]["tooltip_info"] = f"{feature['properties'].get('name', 'Unknown')}"

# Main Content
st.title(f"溫度分布圖 - {selected_date}")

cols = st.columns(len(daily_df))
for idx, row in enumerate(daily_df.itertuples()):
    with cols[idx % 3]: 
        st.metric(
            label=row.region,
            value=f"{row.min_temp}°C - {row.max_temp}°C",
            delta=row.weather_desc
        )

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("台灣氣溫分佈 (行政區界)")
    
    view_state = pdk.ViewState(
        latitude=23.7,
        longitude=121.0,
        zoom=7,
        pitch=0,
    )

    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color="properties.fill_color",
        get_line_color=[255, 255, 255],
        get_line_width=2000,
        pickable=True,
        auto_highlight=True,
    )

    tooltip = {
        "html": "<b>{tooltip_info}</b>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=None 
    )
    
    st.pydeck_chart(r)

with col2:
    st.subheader("地區資訊")
    for _, row in daily_df.iterrows():
        with st.expander(row['region'], expanded=True):
            st.write(f"**氣溫**: {row['min_temp']} ~ {row['max_temp']} °C")
            st.write(f"**天氣**: {row['weather_desc']}")
