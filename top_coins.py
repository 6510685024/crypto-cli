import requests
# import json # ไม่ได้ใช้

def get_top_coins(currency='usd', top_n=10, sort_by='market_cap', api_key=None):
    """ดึงข้อมูลเหรียญคริปโตเคอร์เรนซีตาม Market Cap หรือ Volume."""
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    
    params = {
        'vs_currency': currency,
        'order': f"{sort_by}_desc",
        'per_page': top_n,
        'page': 1,
        'sparkline': 'false'
    }

    if api_key:
        params['x_cg_demo_api_key'] = api_key
        # print("Using CoinGecko API Key in get_top_coins") # << เอาออก หรือ comment
    
    # print(f"API URL: {url}") # << url ไม่ได้ถูก define ใน scope นี้, ควรจะเป็น base_url และ params
    # print(f"Debug: Calling API with URL: {base_url} and params: {params}") # << เอาออก หรือ comment

    try:
        response = requests.get(base_url, params=params)
        # print(f"API Response Status Code: {response.status_code}") # << เอาออก หรือ comment
        response.raise_for_status()
        data = response.json()
        # print("Data received from API:") # << เอาออก หรือ comment
        # print(data) # << เอาออก หรือ comment (ข้อมูลดิบเยอะมาก)
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"Error calling CoinGecko API (HTTP Error): {http_err}")
        if response is not None:
            try:
                error_detail = response.json()
                print(f"API Error Detail: {error_detail.get('error', 'No specific error message from API.')}")
            except ValueError:
                 print("API Error Detail: Could not parse error response from API.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling CoinGecko API (Request Exception): {e}")
        return None
    except ValueError: 
        print(f"Error: Could not decode JSON response from CoinGecko API.")
        return None

# (ส่วน if __name__ == '__main__': สำหรับทดสอบ ยังคงเดิมได้)