# detail.py
import requests

BASE_API_URL_DETAIL = "https://api.coingecko.com/api/v3" # สามารถใช้ BASE_API_URL จาก main.py ได้ถ้า import มา

def get_coin_data(coin_id, api_key=None): # << เพิ่ม api_key เป็น parameter
    """
    Fetches raw detailed coin data from CoinGecko API.
    Returns the full JSON data dictionary on success, None on failure.
    """
    processed_coin_id = coin_id.lower()
    endpoint = f"{BASE_API_URL_DETAIL}/coins/{processed_coin_id}"
    
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true', # สำคัญมาก
        'community_data': 'false', # ตั้งเป็น false ถ้าไม่ต้องการ
        'developer_data': 'false', # ตั้งเป็น false ถ้าไม่ต้องการ
        'sparkline': 'false'
    }

    if api_key:
        params['x_cg_demo_api_key'] = api_key # ใช้ API Key ที่รับมา

    # print(f"DEBUG [detail.py]: Calling API: {endpoint} with params: {params}") 

    try:
        response = requests.get(endpoint, params=params)
        # print(f"DEBUG [detail.py]: API Status Code: {response.status_code}")
        response.raise_for_status() # ตรวจสอบ HTTP errors
        data = response.json() # คืน JSON data ทั้งหมดที่ได้จาก API
        # print(f"DEBUG [detail.py]: API Data Received (first 200 chars): {str(data)[:200]}")
        return data 
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR [detail.py]: HTTP error for '{processed_coin_id}': {http_err}")
        # (สามารถเพิ่มการ print error detail จาก response.json() ที่นี่ได้ถ้าต้องการ)
        return None # คืน None ชัดเจนเมื่อเกิด error
    except requests.exceptions.RequestException as e:
        print(f"ERROR [detail.py]: Request error for '{processed_coin_id}': {e}")
        return None
    except ValueError as json_err: # JSONDecodeError
        print(f"ERROR [detail.py]: JSON decode error for '{processed_coin_id}': {json_err}")
        return None

def handle_detail(coin_id, api_key=None): # api_key ถูกส่งต่อมาจาก main.py
    """
    Wrapper function that calls get_coin_data.
    (ในกรณีนี้ อาจจะดูเหมือนซ้ำซ้อน แต่ถ้า handle_detail ต้องทำอะไรมากกว่าแค่เรียก get_coin_data ก็จะมีประโยชน์)
    """
    # print(f"DEBUG [detail.py -> handle_detail]: Received coin_id: {coin_id}, api_key: {'Yes' if api_key else 'No'}")
    data = get_coin_data(coin_id, api_key=api_key) # << ส่ง api_key ต่อไปให้ get_coin_data
    return data # คืนค่าที่ได้จาก get_coin_data โดยตรง