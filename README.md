# CWA 氣象儀表板專案 (CRISP-DM)

本專案採用 CRISP-DM (跨行業資料探勘標準流程) 方法論，實作了一個針對台灣農業氣象預報的視覺化儀表板。

**Demo Site**: [https://scrapingweather-klynf4ge8hyjxgqt3ujybs.streamlit.app/](https://scrapingweather-klynf4ge8hyjxgqt3ujybs.streamlit.app/)

## 專案結構
```text
D:.
│   .env                  # 環境變數 (API 金鑰)
│   .gitignore            # Git 忽略設定檔
│   app.py                # 資料獲取 (爬蟲程式)
│   dashboard.py          # 部署 (Streamlit 儀表板)
│   geojson_map_data.py   # 資料準備 (GeoJSON 處理)
│   init_db.py            # 資料準備 (資料庫初始化與 ETL)
│   prompt.log            # 對話與流程紀錄
│   requirements.txt      # Python 相依套件
│   taiwan_geo.json       # 原始 GeoJSON 資料 (台灣縣市界)
│   taiwan_map_data.py    # (已棄用) 手動多邊形資料
│   weather.db            # SQLite 資料庫
│   weather_data.json     # 原始氣象資料 (JSON)
│   資料分析.md           # 資料理解文件
│
└───venv                  # Python 虛擬環境
```

## 1. 業務理解 (Business Understanding)
*   **目標**: 提供台灣農業氣象預報的視覺化儀表板，讓使用者能輕鬆檢視六大區域的溫度分佈與天氣描述。
*   **需求**:
    *   從 CWA 開放資料 API 獲取最新氣象資料。
    *   將資料結構化儲存以利查詢。
    *   在互動式地圖上，以精確的地理邊界呈現資料。
    *   顯示關鍵指標（最低/最高溫、天氣描述）。

## 2. 資料理解 (Data Understanding)
*   **來源**: 中央氣象署 (CWA) 開放資料 API (`F-A0010-001`)。
*   **格式**: JSON。
*   **關鍵屬性** (詳見 `資料分析.md`):
    *   `locationName`: 地區名稱 (如：北部地區)。
    *   `weatherElements`: 包含每日預報的 `Wx` (天氣描述)、`MaxT` (最高溫)、`MinT` (最低溫)。
*   **資料結構**: 分層的 JSON 格式，需要解析以提取每日的分區指標。

## 3. 資料準備 (Data Preparation)
*   **ETL 流程** (`init_db.py`):
    *   **擷取 (Extract)**: 使用 `app.py` 抓取 JSON 資料。
    *   **轉換 (Transform)**: 解析 JSON 以提取各區域每日氣象指標。將特定的地區名稱映射至 SQLite 用法。
    *   **載入 (Load)**: 將清理後的資料寫入 `weather.db` (SQLite)，包含 `regions` 與 `forecasts` 資料表。
*   **地理空間資料準備** (`geojson_map_data.py`):
    *   來源：`taiwan_geo.json` (2010 台灣縣市界)。
    *   將各縣市對應至六大天氣區域 (例如：台北市 -> 北部地區)。
    *   聚合/標記 GeoJSON 特徵，加入區域名稱與視覺化顏色代碼。

## 4. 模型建立 (Modeling)
*   *註：在本應用情境中，「模型」指資料邏輯與關聯規則，而非預測性機器學習模型。*
*   **邏輯**:
    *   **聚合視覺化**: 將 22 個行政縣市歸類為 6 個天氣區域。
    *   **顏色映射**: 使用線性插值邏輯，將平均氣溫 (15°C - 30°C) 映射為 藍色-紅色 的漸層色彩。
    *   參見 `dashboard.py` 中的 `get_color(temp)` 函式。

## 5. 評估 (Evaluation)
*   **驗證**:
    *   透過 SQL 查詢驗證資料庫紀錄 (筆數檢查、schema 檢查)。
    *   視覺化驗證儀表板是否符合參考設計。
    *   確認地圖上的縣市與區域映射是否正確 (例如：宜蘭顯示為東北部地區)。
*   **結果**: 儀表板成功呈現固定視角的台灣地圖，具備精確的區域邊界，並從 SQLite 資料庫正確綁定資料。

## 6. 部署 (Deployment)
*   **平台**: Streamlit。
*   **應用程式**: `dashboard.py`。
*   **功能**:
    *   互動式側邊欄：日期選擇。
    *   主儀表板：各地區氣象卡片。
    *   基於 PyDeck 的地理空間地圖：在台灣實際行政邊界上疊加氣象數據。
*   **執行方式**:
    ```bash
    streamlit run dashboard.py
    ```
