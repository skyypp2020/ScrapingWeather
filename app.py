import requests
import json

def download_weather_data():
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&downloadType=WEB&format=JSON"
    output_filename = "F-A0010-001.json"

    try:
        print(f"Start downloading data from {url}...")
        response = requests.get(url)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Save the content to a file
        with open(output_filename, "wb") as f:
            f.write(response.content)
        
        print(f"Successfully downloaded and saved to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")

if __name__ == "__main__":
    download_weather_data()
