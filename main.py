import argparse
import os
from dotenv import load_dotenv
import top_coins  # Import ไฟล์ top_coins.py

# โหลด environment variables จากไฟล์ .env
# ควรทำตั้งแต่ต้นๆ ของสคริปต์ เพื่อให้ตัวแปรพร้อมใช้งาน
load_dotenv()

# ดึง API Key จาก environment variable
# ถ้าไม่มีการตั้งค่า COINGECKO_API_KEY ใน .env หรือ environment จริง
# ตัวแปรนี้จะเป็น None ซึ่งเราสามารถจัดการได้ในฟังก์ชันที่เรียก API
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# URL พื้นฐานของ CoinGecko API (สามารถย้ายไปไว้ในฟังก์ชันที่เรียก API ได้ถ้าต้องการ)
BASE_API_URL = "https://api.coingecko.com/api/v3"

def main():
    print("Main function started.") # top_coins เพิ่มอันนี้
    parser = argparse.ArgumentParser(
        description="Crypto CLI - Fetch cryptocurrency data from CoinGecko API."
    )
    subparsers = parser.add_subparsers(dest="command", title="Available Commands", help="Sub-command help")
    subparsers.required = True # ทำให้ต้องมี subcommand เสมอ

    # --- Subcommand: price (จะถูก implement ใน feature/get-price branch) ---
    # price_parser = subparsers.add_parser("price", help="Get the current price of a coin.")
    # price_parser.add_argument("coin_id", type=str, help="The ID of the cryptocurrency (e.g., bitcoin, ethereum).")
    # price_parser.add_argument("vs_currency", type=str, help="The currency to compare against (e.g., usd, thb).")

    # --- (Subcommands อื่นๆ จะถูกเพิ่มใน feature branches ของตัวเอง) ---
    # list_parser = subparsers.add_parser("list", help="List available data types or coins.")
    # compare_parser = subparsers.add_parser("compare", help="Compare multiple cryptocurrencies.")
    # ... และอื่นๆ

    # --- Subcommand: top_coins (จะถูก implement ใน feature/top_coins branch) ---
    top_parser = subparsers.add_parser("top", help="Display top N cryptocurrencies.")
    top_parser.add_argument("limit", type=int, default=10, nargs='?', help="Number of top coins to display (default: 10).")
    top_parser.add_argument("--vs_currency", type=str, default="usd", help="The currency to compare against (default: usd).")
    top_parser.add_argument("--sort_by", type=str, default="market_cap", choices=['market_cap', 'volume'], help="Sort by 'market_cap' or 'volume' (default: market_cap).")
    top_parser.set_defaults(func=handle_top_command)

    args = parser.parse_args()

    # --- การจัดการ Command ---
    # if args.command == "price":
    #     # เรียกฟังก์ชันสำหรับ price feature (จะถูกเขียนใน feature/get-price branch)
    #     # handle_price_command(args)
    #     pass
    # elif args.command == "list":
    #     # handle_list_command(args)
    #     pass
    # ... และอื่นๆ

    # ถ้าไม่มี command ไหนถูกเรียก (ซึ่งไม่ควรเกิดถ้า subparsers.required = True)
    # หรือถ้าต้องการให้แสดง help เมื่อไม่มี subcommand เฉพาะเจาะจง
#    if not hasattr(args, 'command') or args.command is None:
#        parser.print_help()
#    elif not any(args.command == cmd for cmd in ["price", "list", "compare", "info", "top"]): # ตัวอย่างการตรวจสอบ
#        print(f"Command '{args.command}' is not yet implemented or recognized.")
#        print("Use -h or --help for available commands.")

# top_coins branch
 # --- การจัดการ Command ---
    if hasattr(args, 'func'):
        args.func(args) # บรรทัดนี้ควรจะเรียก handle_top_command ถ้า 'top' ถูกสั่ง
    elif not hasattr(args, 'command') or args.command is None:
        parser.print_help()
    else:
        print(f"Command '{args.command}' is not yet implemented or recognized.")
        print("Use -h or --help for available commands.")

# top_coins branch
def handle_top_command(args):
    """Handles the 'top' subcommand."""
    print("handle_top_command is being executed.")
    currency = args.vs_currency
    limit = args.limit
    sort = args.sort_by
    data = top_coins.get_top_coins(currency=currency, top_n=limit, sort_by=sort, api_key=COINGECKO_API_KEY)
    if data:
        print("Data received from get_top_coins:")
        print(data) # เพิ่มบรรทัดนี้
        print(f"Top {limit} coins sorted by {sort.replace('_', ' ').title()} ({currency.upper()}):")
        for i, coin in enumerate(data):
            print(f"{i+1}. {coin['name']} ({coin['symbol'].upper()}): Price: ${coin['current_price']:,}, Market Cap: ${coin['market_cap']:,}, Volume: ${coin['total_volume']:,}")


if __name__ == "__main__":
    if COINGECKO_API_KEY is None:
        print("Warning: COINGECKO_API_KEY not found in .env file or environment variables.")
        print("Some features might not work correctly or might be rate-limited.")
        print("Please create a .env file with COINGECKO_API_KEY='your_api_key_here'.")
        print("-" * 30)
    main()