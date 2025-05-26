import argparse
import os
import requests
from dotenv import load_dotenv
from compare import handle_compare_command # << ตรวจสอบว่าชื่อไฟล์และฟังก์ชันถูกต้อง
import top_coins 

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# ดึง API Key จาก environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# URL พื้นฐานของ CoinGecko API
BASE_API_URL = "https://api.coingecko.com/api/v3"

# --- ฟังก์ชันสำหรับ Feature 'price' ---
def get_coin_price_data(coin_id, vs_currency):
    # ... (โค้ด get_coin_price_data เหมือนเดิม) ...
    endpoint = f"{BASE_API_URL}/simple/price"
    params = { 'ids': coin_id, 'vs_currencies': vs_currency}
    if COINGECKO_API_KEY:
        params['x_cg_demo_api_key'] = COINGECKO_API_KEY
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if coin_id in data and vs_currency in data[coin_id]:
            return data[coin_id][vs_currency]
        else:
            print(f"Error: Could not retrieve price for '{coin_id}' in '{vs_currency}'.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An API request error occurred: {req_err}")
    except ValueError:
        print("Error: Could not decode JSON response from API.")
    return None

def handle_price_command(args):
    price = get_coin_price_data(args.coin_id.lower(), args.vs_currency.lower())
    if price is not None:
        print(f"The current price of {args.coin_id.capitalize()} is: {price} {args.vs_currency.upper()}")

# --- ฟังก์ชันสำหรับ Feature 'list' ---
def get_top_coins_list_data(limit=10, vs_currency='thb'):
    # ... (โค้ด get_top_coins_list_data เหมือนเดิม) ...
    endpoint = f"{BASE_API_URL}/coins/markets"
    params = {'vs_currency': vs_currency, 'order': 'market_cap_desc', 'per_page': limit, 'page': 1, 'sparkline': 'false'}
    if COINGECKO_API_KEY:
        params['x_cg_demo_api_key'] = COINGECKO_API_KEY
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching top coins list: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"API request error for top coins list: {e}")
    except ValueError:
        print("Error: Could not decode JSON response for top coins list.")
    return None

def handle_list_command(args):
    # ... (โค้ด handle_list_command เหมือนเดิม) ...
    coins_data = get_top_coins_list_data(limit=args.limit, vs_currency=args.currency.lower())
    if coins_data:
        print(f"\nTop {args.limit} coins by Market Cap in {args.currency.upper()}...\n")
        print(f"{'Rank':<5} {'Name':<25} {'Symbol':<10} {'Price':<15} {'Market Cap':<20}")
        print("-" * 80)
        for i, coin in enumerate(coins_data):
            rank = i + 1
            name = coin.get('name', 'N/A')
            symbol = coin.get('symbol', 'N/A').upper()
            price_val = coin.get('current_price', 'N/A')
            market_cap = coin.get('market_cap', 'N/A')
            price_str = f"{price_val:,}" if isinstance(price_val, (int, float)) else str(price_val)
            market_cap_str = f"{market_cap:,}" if isinstance(market_cap, (int, float)) else str(market_cap)
            print(f"{rank:<5} {name:<25} {symbol:<10} {price_str:<15} {market_cap_str:<20}")
    else:
        print("No data received for the list of top coins.")


# --- ฟังก์ชันสำหรับ Feature 'top_coins' ---
def handle_top_command(args):
    # ... (โค้ด handle_top_command เหมือนเดิม, ตรวจสอบการจัดการ args.limit ถ้ายังใช้ nargs='?') ...
    currency = args.vs_currency.lower()
    limit = args.limit
    if isinstance(limit, list) and limit: # จัดการกรณี nargs='?' ที่อาจจะยังหลงเหลือ
        limit = limit[0]
    elif limit is None :
         limit = 10 # ควรมาจาก default ของ argparse
    sort = args.sort_by
    data = top_coins.get_top_coins(currency=currency, top_n=limit, sort_by=sort, api_key=COINGECKO_API_KEY)
    if data:
        print(f"\nTop {limit} Coins (Sorted by {sort.replace('_', ' ').title()}) in {currency.upper()}:")
        print(f"{'Rank':<5} {'Name':<25} {'Symbol':<10} {'Price':<15} {'Market Cap':<20} {'Volume (24h)':<20}")
        print("-" * 100)
        for i, coin in enumerate(data):
            rank = i + 1
            name = coin.get('name', 'N/A')
            symbol = coin.get('symbol', 'N/A').upper()
            price_val = coin.get('current_price', 'N/A')
            market_cap_val = coin.get('market_cap', 'N/A')
            volume_val = coin.get('total_volume', 'N/A')
            price_str = f"{price_val:,.2f}" if isinstance(price_val, (int, float)) else str(price_val)
            market_cap_str = f"{market_cap_val:,}" if isinstance(market_cap_val, (int, float)) else str(market_cap_val)
            volume_str = f"{volume_val:,}" if isinstance(volume_val, (int, float)) else str(volume_val)
            print(f"{rank:<5} {name:<25} {symbol:<10} {price_str:<15} {market_cap_str:<20} {volume_str:<20}")
    else:
        print("No data received from top_coins.get_top_coins.")

# (ถ้า feature compare มีฟังก์ชัน data getter แยก ก็ควรจะ define ไว้แถวนี้ หรือ import มา)
# from compare import get_compare_data # ตัวอย่าง

def main():
    parser = argparse.ArgumentParser(
        description="Crypto CLI - Fetch cryptocurrency data from CoinGecko API."
    )
    subparsers = parser.add_subparsers(title="Available Commands", help="Sub-command help", required=True)

    # --- Subcommand: price ---
    price_parser = subparsers.add_parser("price", help="Get the current price of a coin.")
    price_parser.add_argument("coin_id", type=str, help="The ID of the cryptocurrency (e.g., bitcoin, ethereum).")
    price_parser.add_argument("vs_currency", type=str, help="The currency to compare against (e.g., usd, thb).")
    price_parser.set_defaults(func=handle_price_command)

    # --- Subcommand: list ---
    list_parser = subparsers.add_parser("list", help="List top N cryptocurrencies by market cap.")
    list_parser.add_argument("--limit", type=int, default=10, help="Number of top coins to display (default: 10).")
    list_parser.add_argument("--currency", type=str, default="thb", help="The currency for price and market cap display (default: thb).")
    list_parser.set_defaults(func=handle_list_command)

    # --- Subcommand: top ---
    top_parser = subparsers.add_parser("top", help="Display top N cryptocurrencies with sorting.")
    top_parser.add_argument("--limit", type=int, default=10, help="Number of top coins to display (default: 10).")
    top_parser.add_argument("--vs_currency", type=str, default="usd", help="The currency to compare against (default: usd).")
    top_parser.add_argument("--sort-by", type=str, default="market_cap", choices=['market_cap', 'volume'], help="Sort by 'market_cap' or 'volume' (default: market_cap).")
    top_parser.set_defaults(func=handle_top_command)

    # --- Subcommand: compare (เพิ่มเข้ามา) ---
    compare_parser = subparsers.add_parser("compare", help="Compare multiple cryptocurrencies.")
    compare_parser.add_argument("coins", nargs="+", help="List of coin IDs to compare (e.g., bitcoin ethereum)") # 'coins' คือชื่อ argument ที่จะเก็บ list ของ coin IDs
    compare_parser.add_argument("vs_currency", help="The currency to compare against (e.g., usd, thb)") # 'vs_currency' คือชื่อ argument สำหรับสกุลเงิน
    compare_parser.set_defaults(func=handle_compare_command) # << สำคัญมาก!

    # --- (Subcommands อื่นๆ สามารถเพิ่มตามแพทเทิร์นนี้) ---

    args = parser.parse_args() # เรียก parse_args เพียงครั้งเดียว

    # --- การจัดการ Command (ตามโครงสร้าง `args.func`) ---
    if hasattr(args, 'func'):
        args.func(args)
    else: # ส่วนนี้ควรจะถูกเรียกเฉพาะถ้ามี bug ในการตั้งค่า parser หรือ command ไม่ได้ผูก func
        print(f"Error: Command '{args.command if hasattr(args, 'command') else 'None'}' could not be processed.")
        print("Please ensure the command is valid and implemented correctly.")
        parser.print_help()


if __name__ == "__main__":
    # ส่วน comment out การตรวจสอบ COINGECKO_API_KEY สามารถนำกลับมาได้ถ้าต้องการ
    '''if COINGECKO_API_KEY is None:
        print("Warning: COINGECKO_API_KEY not found in .env file or environment variables.")
        print("Some features might not work correctly or might be rate-limited.")
        print("Please create a .env file with COINGECKO_API_KEY='your_api_key_here'.")
        print("-" * 30)'''
    main()