
import json

# Mapping of County Name to Region Name
# Adjust names based on the actual GeoJSON properties (usually 'name' or 'COUNTYNAME')
COUNTY_TO_REGION = {
    "臺北市": "北部地區",
    "新北市": "北部地區",
    "基隆市": "北部地區",
    "桃園市": "北部地區",
    "新竹市": "北部地區",
    "新竹縣": "北部地區",
    "苗栗縣": "北部地區",
    
    "臺中市": "中部地區",
    "彰化縣": "中部地區",
    "南投縣": "中部地區",
    "雲林縣": "中部地區",
    "嘉義市": "中部地區",
    "嘉義縣": "中部地區",
    
    "臺南市": "南部地區",
    "高雄市": "南部地區",
    "屏東縣": "南部地區",
    "澎湖縣": "南部地區", # Often part of South in simplified forecasts or separate. Assuming South here.
    
    "宜蘭縣": "東北部地區",
    
    "花蓮縣": "東部地區",
    
    "臺東縣": "東南部地區",
    
    # Islands (might need exclusion or mapping if present)
    "金門縣": "其他",
    "連江縣": "其他"
}

def load_and_process_geojson():
    with open("taiwan_geo.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    processed_features = []
    
    for feature in data["features"]:
        props = feature["properties"]
        # Try to find name property
        name = props.get("name") or props.get("COUNTYNAME") or props.get("COUNTYENG")
        
        if not name:
            continue
            
        # Handle some renaming if legacy names exist (e.g. Taipei County -> New Taipei City if old data)
        # But twCounty2010 should be decent.
        # Check mapping
        region = COUNTY_TO_REGION.get(name)
        if not region:
            # Try removing 'City'/'County' suffix logic if simple match fails, 
            # but usually exact match is best for known sets.
            continue
            
        # Add region info to properties
        feature["properties"]["region"] = region
        processed_features.append(feature)
        
    return {"type": "FeatureCollection", "features": processed_features}

if __name__ == "__main__":
    # Test
    out = load_and_process_geojson()
    print(f"Processed {len(out['features'])} features.")
