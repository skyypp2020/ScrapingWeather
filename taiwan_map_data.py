
# Approximate simplified polygons for Taiwan's 6 Weather Regions
# Coordinates format: [Longitude, Latitude]

# Northern (Taipei, New Taipei, Keelung, Taoyuan, Hsinchu, Miaoli)
NORTH_POLY = [
    [121.5, 25.3], [121.9, 25.1], [122.0, 25.0],  # Top Tip & Right
    [121.5, 24.5], [121.0, 24.5], [120.9, 24.5], # Bottom boundary with Central
    [120.7, 24.6], [120.9, 25.1], [121.3, 25.2], [121.5, 25.3] # West coast & Top
]

# Northeastern (Yilan)
NORTHEAST_POLY = [
    [121.6, 25.0], # Top boundary with North
    [122.0, 25.0], [121.9, 24.3], # East coast
    [121.3, 24.3], # Bottom boundary
    [121.3, 24.6], [121.6, 25.0]  # Left boundary
]

# Central (Taichung, Changhua, Nantou, Yunlin, Chiayi)
CENTRAL_POLY = [
    [120.9, 24.5], [121.3, 24.5], # Top boundary with North/NE
    [121.3, 23.5], # Right boundary (Central Mt Range)
    [120.1, 23.5], # Bottom boundary with South
    [120.1, 23.9], [120.5, 24.2], [120.9, 24.5] # West coast
]

# Eastern (Hualien)
EAST_POLY = [
    [121.3, 24.3], [121.9, 24.3], # Top boundary with NE
    [121.6, 23.5], # East Coast
    [121.4, 23.5], # Bottom boundary
    [121.3, 24.3]  # Left boundary (Central Mt Range)
]

# Southern (Tainan, Kaohsiung, Pingtung)
# Needs to wrap around the bottom slightly
SOUTH_POLY = [
    [120.1, 23.5], [120.7, 23.5], # Top boundary with Central
    [120.7, 22.0], # Right boundary 
    [120.9, 21.9], [120.8, 21.8], # Tip
    [120.2, 22.5], [120.0, 23.0], [120.1, 23.5] # West coast
]

# Southeastern (Taitung)
SOUTHEAST_POLY = [
    [120.7, 23.5], [121.4, 23.5], # Top boundary with Central/East
    [121.6, 23.5], [121.5, 22.0], # East Coast
    [120.9, 21.9], # Bottom Tip
    [120.7, 22.0], [120.7, 23.5] # Left boundary
]

REGION_POLYGONS = {
    "北部地區": NORTH_POLY,
    "東北部地區": NORTHEAST_POLY,
    "中部地區": CENTRAL_POLY,
    "東部地區": EAST_POLY,
    "南部地區": SOUTH_POLY,
    "東南部地區": SOUTHEAST_POLY
}
