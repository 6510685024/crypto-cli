import argparse
import os
import requests
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# ดึง API Key จาก environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# URL พื้นฐานของ CoinGecko API
BASE_API_URL = "https://api.coingecko.com/api/v3"

def list_top_coins(limit=10, vs_currency='thb'):
    """
    Fetches and lists the top N cryptocurrencies by market cap.
    """
    endpoint = f"{BASE_API_URL}/coins/markets"
    params = {
        'vs_currency': vs_currency,
        'order': 'market_cap_desc', # เรียงตาม market cap จากมากไปน้อย
        'per_page': limit,          # จำนวนเหรียญที่จะดึง
        'page': 1,                  # หน้าแรก
        'sparkline': 'false',       # ไม่ต้องการข้อมูล sparkline
        'price_change_percentage': '1h,24h,7d' # ตัวอย่างการขอข้อมูลเพิ่มเติม (optional)
    }
    if COINGECKO_API_KEY:
        params['x_cg_demo_api_key'] = COINGECKO_API_KEY

    print(f"\nFetching Top {limit} coins by Market Cap in {vs_currency.upper()}...\n")

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        coins_data = response.json()

        if not coins_data:
            print("No data received from the API for top coins.")
            return

        print(f"{'Rank':<5} {'Name':<25} {'Symbol':<10} {'Price':<15} {'Market Cap':<20}")
        print("-" * 80)
        for i, coin in enumerate(coins_data):
            rank = i + 1
            name = coin.get('name', 'N/A')
            symbol = coin.get('symbol', 'N/A').upper()
            price = coin.get('current_price', 'N/A')
            market_cap = coin.get('market_cap', 'N/A')
            print(f"{rank:<5} {name:<25} {symbol:<10} {price:<15,} {market_cap:<20,}") # ใช้ , ให้ตัวเลขอ่านง่าย

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching top coins: {http_err}")
        # ... (เพิ่ม error handling ที่เฉพาะเจาะจงได้) ...
    except requests.exceptions.RequestException as e:
        print(f"API request error for top coins: {e}")
    except ValueError: # JSONDecodeError
        print("Error: Could not decode JSON response for top coins.")

# --- END: โค้ดสำหรับ Feature 'list' ---


def main():
    parser = argparse.ArgumentParser(
        description="Crypto CLI - Fetch cryptocurrency data from CoinGecko API."
    )
    subparsers = parser.add_subparsers(dest="command", title="Available Commands", help="Sub-command help")
    subparsers.required = True

    # --- Subcommand: price (จาก feature/get-price หรือ main) ---
    price_parser = subparsers.add_parser("price", help="Get the current price of a coin.")
    price_parser.add_argument("coin_id", type=str, help="The ID of the cryptocurrency (e.g., bitcoin, ethereum).")
    price_parser.add_argument("vs_currency", type=str, help="The currency to compare against (e.g., usd, thb).")

    # --- Subcommand: list ---
    list_parser = subparsers.add_parser("list", help="List top N cryptocurrencies by market cap.")
    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of top coins to display (default: 10)."
    )
    list_parser.add_argument(
        "--currency",
        type=str,
        default="thb",
        help="The currency for price and market cap display (default: thb)."
    )
    # (สามารถเพิ่ม options อื่นๆ ได้ เช่น --sort-by volume)


    # --- (Subcommands อื่นๆ จะถูกเพิ่มใน feature branches ของตัวเอง) ---

    args = parser.parse_args()

    # --- การจัดการ Command ---
    if args.command == "price":
        price_val = get_coin_price(args.coin_id.lower(), args.vs_currency.lower())
        if price_val is not None:
            print(f"The current price of {args.coin_id.capitalize()} is: {price_val} {args.vs_currency.upper()}")

    elif args.command == "list":
        list_top_coins(limit=args.limit, vs_currency=args.currency.lower())

    else:
        print(f"Command '{args.command}' is recognized but not yet fully implemented for execution.")
        parser.print_help()


if __name__ == "__main__":
    if COINGECKO_API_KEY is None:
        print("Warning: COINGECKO_API_KEY not found in .env file or environment variables.")
        print("Some features might not work correctly or might be rate-limited.")
        print("Please create a .env file with COINGECKO_API_KEY='your_api_key_here'.")
        print("-" * 30)
    main()