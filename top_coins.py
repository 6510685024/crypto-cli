import requests
import json

def get_top_coins(currency='usd', top_n=10, sort_by='market_cap', api_key=None):
    """ดึงข้อมูลเหรียญคริปโตเคอร์เรนซีตาม Market Cap หรือ Volume."""
    headers = {}
    if api_key:
        headers['x-cg-api-key'] = api_key
        print("Using CoinGecko API Key in get_top_coins") # Optional

    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order={sort_by}_desc&per_page={top_n}"
    print(f"API URL: {url}") # ดู URL ที่เรียก

    try:
        response = requests.get(url, headers=headers)
        print(f"API Response Status Code: {response.status_code}") # ดู Status Code
        response.raise_for_status()
        data = response.json()
        print("Data received from API:")
        print(data) # ดูข้อมูลดิบที่ได้รับ
        return data
    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาดในการเรียก API: {e}")
        return None