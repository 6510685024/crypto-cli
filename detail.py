import requests

def get_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'],
            'symbol': data['symbol'],
            'current_price': data['market_data']['current_price']['usd'],
            'market_cap': data['market_data']['market_cap']['usd'],
            'total_volume': data['market_data']['total_volume']['usd'],
            'homepage': data['links']['homepage'][0]
        }
    elif response.status_code == 404:
        raise ValueError(f"'{coin_id}'was not found")
    else:
        raise ConnectionError("An error occurred while fetching data from the API.")

def handle_detail(coin_id):
    """
    ดึงข้อมูลเหรียญจาก CoinGecko API
    :param coin_id: เช่น bitcoin, ethereum
    :return: dict ข้อมูลเหรียญ
    """
    try:
        data = get_coin_data(coin_id)
        return data
    except ValueError as ve:
        print(ve)
    except ConnectionError as ce:
        print(ce)