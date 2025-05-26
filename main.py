import argparse
import os
import requests # เพิ่ม requests
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# ดึง API Key จาก environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# URL พื้นฐานของ CoinGecko API
BASE_API_URL = "https://api.coingecko.com/api/v3"

def get_coin_price(coin_id, vs_currency):
    """
    Fetches the current price of a given cryptocurrency in a specified currency
    using the CoinGecko API.
    """
    endpoint = f"{BASE_API_URL}/simple/price"
    params = {
        'ids': coin_id,
        'vs_currencies': vs_currency,
    }
    # เพิ่ม API Key ถ้ามี
    if COINGECKO_API_KEY:
        params['x_cg_demo_api_key'] = COINGECKO_API_KEY # สำหรับ Demo Key
        # params['x_cg_pro_api_key'] = COINGECKO_API_KEY # ถ้าเป็น Pro Key

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4XX or 5XX)
        data = response.json()

        if coin_id in data and vs_currency in data[coin_id]:
            price = data[coin_id][vs_currency]
            return price
        else:
            print(f"Error: Could not retrieve price for '{coin_id}' in '{vs_currency}'.")
            print("Ensure the coin ID and currency symbol are correct and supported by the API.")
            if not data: # API อาจจะตอบกลับ {} ถ้าไม่เจอ coin_id
                 print(f"Debug: API response for '{coin_id}' was empty.")
            elif coin_id not in data:
                 print(f"Debug: Coin ID '{coin_id}' not found in API response: {list(data.keys())}")
            elif vs_currency not in data.get(coin_id, {}):
                 print(f"Debug: Currency '{vs_currency}' not found for coin '{coin_id}' in API response: {data.get(coin_id, {})}")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response is not None: # ตรวจสอบว่า response object มีค่าก่อนใช้งาน
            if response.status_code == 401 or response.status_code == 403:
                print("Detail: Authentication error. Check your API Key (COINGECKO_API_KEY).")
            elif response.status_code == 404:
                print(f"Detail: Coin ID '{coin_id}' or currency '{vs_currency}' might not be found or supported.")
            elif response.status_code == 429:
                print("Detail: API rate limit exceeded. Please wait and try again later, or check your API plan.")
            else:
                try:
                    error_detail = response.json()
                    print(f"API Error Detail: {error_detail.get('error', 'No specific error message from API.')}")
                except ValueError:
                    print("API Error Detail: Could not parse error response from API.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An API request error occurred: {req_err}")
    except ValueError: # JSONDecodeError
        print("Error: Could not decode JSON response from API. The API might be down or returning unexpected data.")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Crypto CLI - Fetch cryptocurrency data from CoinGecko API."
    )
    subparsers = parser.add_subparsers(dest="command", title="Available Commands", help="Sub-command help")
    subparsers.required = True

    # --- Subcommand: price ---
    price_parser = subparsers.add_parser("price", help="Get the current price of a coin.")
    price_parser.add_argument("coin_id", type=str, help="The ID of the cryptocurrency (e.g., bitcoin, ethereum).")
    price_parser.add_argument("vs_currency", type=str, help="The currency to compare against (e.g., usd, thb).")

    # --- (Subcommands อื่นๆ จะถูกเพิ่มใน feature branches ของตัวเอง) ---

    args = parser.parse_args()

    # --- การจัดการ Command ---
    if args.command == "price":
        price = get_coin_price(args.coin_id.lower(), args.vs_currency.lower())
        if price is not None:
            print(f"The current price of {args.coin_id.capitalize()} is: {price} {args.vs_currency.upper()}")
    # elif args.command == "list":
    #     pass # Implement list command here
    else:
        # ในกรณีที่เพิ่ม subcommand ใหม่ๆ แต่ยังไม่ได้ handle ใน if-elif นี้
        print(f"Command '{args.command}' is recognized but not yet fully implemented for execution.")
        parser.print_help()


if __name__ == "__main__":
    if COINGECKO_API_KEY is None:
        print("Warning: COINGECKO_API_KEY not found in .env file or environment variables.")
        print("Some features might not work correctly or might be rate-limited.")
        print("Please create a .env file with COINGECKO_API_KEY='your_api_key_here'.")
        print("-" * 30)
    main()