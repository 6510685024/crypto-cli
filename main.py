import argparse
import os
import sys # เพิ่ม sys สำหรับ sys.argv และ sys.exit
import requests
from dotenv import load_dotenv

# Import handlers/modules จากไฟล์อื่นๆ
from detail import handle_detail # สมมติว่า detail.py มีฟังก์ชันนี้ที่คืนข้อมูล
from compare import handle_compare_command 
import top_coins # สมมติว่า top_coins.py มี get_top_coins

# Import Rich library components
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table # เพิ่ม Table สำหรับการแสดงผลที่สวยงามขึ้น

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# ดึง API Key จาก environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# URL พื้นฐานของ CoinGecko API
BASE_API_URL = "https://api.coingecko.com/api/v3"

# สร้าง Rich Console object สำหรับการแสดงผล
console = Console()
panel_width = 80 # ความกว้างของ Panel

# --- ฟังก์ชัน Handler สำหรับแต่ละ Subcommand ---

def handle_price_command(args):
    """Handles the 'price' subcommand."""
    endpoint = f"{BASE_API_URL}/simple/price"
    params = {'ids': args.coin_id.lower(), 'vs_currencies': args.vs_currency.lower()}
    if COINGECKO_API_KEY:
        params['x_cg_demo_api_key'] = COINGECKO_API_KEY

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        coin_id_key = args.coin_id.lower() # ใช้ key ที่ถูกต้อง
        currency_key = args.vs_currency.lower()

        if coin_id_key in data and currency_key in data[coin_id_key]:
            price = data[coin_id_key][currency_key]
            price_text = Text(f"The current price of ", style="green")
            price_text.append(args.coin_id.capitalize(), style="bold cyan")
            price_text.append(f" is: ", style="green")
            price_text.append(f"{price:,.2f} {args.vs_currency.upper()}", style="bold yellow")
            console.print(Panel(price_text, title="💰 Coin Price", width=panel_width, border_style="green"))
        else:
            console.print(Panel(Text(f"Error: Could not retrieve price for '{args.coin_id}' in '{args.vs_currency}'.\nPlease ensure the coin ID (e.g., 'bitcoin') and currency symbol are correct.", style="bold red"), title="Error", width=panel_width))
            # console.print(f"Debug data: {data}") # Uncomment for debugging
    except requests.exceptions.HTTPError as http_err:
        console.print(Panel(Text(f"HTTP error occurred: {http_err}", style="bold red"), title="API Error", width=panel_width))
    except requests.exceptions.RequestException as req_err:
        console.print(Panel(Text(f"API request error occurred: {req_err}", style="bold red"), title="Request Error", width=panel_width))
    except ValueError:
        console.print(Panel(Text("Error: Could not decode JSON response from API.", style="bold red"), title="JSON Error", width=panel_width))


def handle_list_command(args):
    """Displays the types of data/features available from the application."""
    list_text_content = Text()
    list_text_content.append("📊 Available Data Types & Features:\n\n", style="bold #FFD700 underline")
    
    features_info = [
        ("Current Price", "View the current price of a specific cryptocurrency."),
        ("Top Coins List", "List top N cryptocurrencies diversitéd by market capitalization."),
        ("Sorted Top Coins", "Display top N cryptocurrencies with sorting by market cap or volume."),
        ("Coin Comparison", "Compare market data across multiple specified cryptocurrencies."),
        ("Detailed Coin Info", "Show comprehensive information for a single cryptocurrency."),
        ("Help Information", "Display the help message listing all commands and usage examples.")
    ]
    
    for i, (feature_name, description) in enumerate(features_info, 1):
        list_text_content.append(f"{i}. {feature_name}:\n", style="bold cyan")
        list_text_content.append(f"   {description}\n\n", style="white")
    
    console.print(Panel(list_text_content, title="[bold #20B2AA]Application Capabilities[/]", width=panel_width, border_style="#20B2AA", expand=False))

def handle_top_command(args):
    """Handles the 'top' subcommand (flexible sorting)."""
    currency = args.vs_currency.lower()
    limit = args.limit
    # จัดการ args.limit ถ้ามันถูกตั้งค่า nargs='?' (แต่เราเอาออกไปแล้วในการประกาศ parser)
    # if isinstance(limit, list) and limit: limit = limit[0]
    # elif limit is None: limit = 10 
    
    sort = args.sort_by
    
    # เรียกฟังก์ชันจากไฟล์ top_coins.py
    data = top_coins.get_top_coins(currency=currency, top_n=limit, sort_by=sort, api_key=COINGECKO_API_KEY)

    if data:
        table = Table(title=f"📊 Top {limit} Coins (Sorted by {sort.replace('_', ' ').title()}) ({currency.upper()})", show_header=True, header_style="bold magenta", width=panel_width + 16) # เพิ่มความกว้างสำหรับ volume
        table.add_column("Rank", style="dim", width=6, justify="right")
        table.add_column("Name", style="cyan", width=25)
        table.add_column("Symbol", style="bold yellow", width=10)
        table.add_column(f"Price ({currency.upper()})", style="green", justify="right", width=18)
        table.add_column(f"Market Cap ({currency.upper()})", style="blue", justify="right", width=22)
        table.add_column(f"Volume (24h, {currency.upper()})", style="purple", justify="right", width=22)

        for i, coin in enumerate(data):
            rank = str(i + 1)
            name = coin.get('name', 'N/A')[:23]
            symbol = coin.get('symbol', 'N/A').upper()
            price_val = coin.get('current_price')
            market_cap_val = coin.get('market_cap')
            volume_val = coin.get('total_volume')

            price_str = f"{price_val:,.2f}" if isinstance(price_val, (int, float)) else "N/A"
            market_cap_str = f"{market_cap_val:,}" if isinstance(market_cap_val, (int, float)) else "N/A"
            volume_str = f"{volume_val:,}" if isinstance(volume_val, (int, float)) else "N/A"

            table.add_row(rank, name, symbol, price_str, market_cap_str, volume_str)
        console.print(Panel(table, title="Top Coins Sorted", width=panel_width+20, border_style="yellow"))
    else:
        console.print(Panel(Text(f"No data received from top_coins.get_top_coins for sorting by {sort}.", style="yellow"), title="Info", width=panel_width))


def handle_detail_command(args):
    """Handles the 'detail' subcommand."""
    # เรียกฟังก์ชัน handle_detail จาก detail.py ซึ่งควรจะคืน dictionary ของข้อมูลเหรียญ
    coin_data = handle_detail(args.coin_id, api_key=COINGECKO_API_KEY) # ส่ง API Key ไปด้วย

    if coin_data:
        text_content = Text()
        text_content.append(f"ID           : {coin_data.get('id', 'N/A')}\n", style="white")
        text_content.append(f"Name         : {coin_data.get('name', 'N/A')}\n", style="bold cyan")
        text_content.append(f"Symbol       : {coin_data.get('symbol', 'N/A').upper()}\n", style="bold yellow")
        
        price_usd = coin_data.get('market_data', {}).get('current_price', {}).get('usd', 'N/A')
        price_thb = coin_data.get('market_data', {}).get('current_price', {}).get('thb', 'N/A')
        text_content.append(f"Price (USD)  : ${price_usd:,.2f}\n" if isinstance(price_usd, (int,float)) else f"Price (USD)  : {price_usd}\n", style="green")
        text_content.append(f"Price (THB)  : ฿{price_thb:,.2f}\n" if isinstance(price_thb, (int,float)) else f"Price (THB)  : {price_thb}\n", style="green")

        market_cap_usd = coin_data.get('market_data', {}).get('market_cap', {}).get('usd', 'N/A')
        text_content.append(f"Market Cap   : ${market_cap_usd:,}\n" if isinstance(market_cap_usd, (int,float)) else f"Market Cap   : {market_cap_usd}\n", style="blue")
        
        total_volume_usd = coin_data.get('market_data', {}).get('total_volume', {}).get('usd', 'N/A')
        text_content.append(f"Volume (24h) : ${total_volume_usd:,}\n" if isinstance(total_volume_usd, (int,float)) else f"Volume (24h) : {total_volume_usd}\n", style="purple")

        high_24h_usd = coin_data.get('market_data', {}).get('high_24h', {}).get('usd', 'N/A')
        low_24h_usd = coin_data.get('market_data', {}).get('low_24h', {}).get('usd', 'N/A')
        text_content.append(f"High 24h     : ${high_24h_usd:,.2f}\n" if isinstance(high_24h_usd, (int,float)) else f"High 24h     : {high_24h_usd}\n", style="dim green")
        text_content.append(f"Low 24h      : ${low_24h_usd:,.2f}\n" if isinstance(low_24h_usd, (int,float)) else f"Low 24h      : {low_24h_usd}\n", style="dim red")

        description = coin_data.get('description', {}).get('en', 'No description available.')
        # ตัด description ให้สั้นลงถ้ามันยาวเกินไป
        description_snippet = (description.split('.')[0] + '.') if '.' in description else description
        description_snippet = (description_snippet[:200] + '...') if len(description_snippet) > 200 else description_snippet
        text_content.append(f"Description  : {description_snippet}\n", style="italic")
        
        homepage = coin_data.get('links', {}).get('homepage', ['N/A'])[0]
        text_content.append(f"Homepage     : {homepage}\n", style="link {homepage}")

        console.print(Panel(text_content, title=f"🔎 Coin Detail: {coin_data.get('name', args.coin_id)}", width=panel_width, border_style="magenta"))
    else:
        console.print(Panel(Text(f"Could not retrieve details for coin ID: {args.coin_id}", style="bold red"), title="Error", width=panel_width))


def handle_help_command(args=None): # args=None เพื่อให้ handler สอดคล้องกัน
    """Handles the 'help' subcommand, displaying custom help."""
    help_text_content = Text()
    help_text_content.append("📚 Crypto Command Line Interface 📚\n\n", style="bold #1E90FF underline")
    help_text_content.append("Available commands:\n", style="bold #FFA500")
    
    commands_info = [
        ("price <coin_id> <vs_currency>", "Get the current price of a specific coin (e.g., price bitcoin usd)."),
        ("list [--limit N] [--currency CUR]", "List top N coins by market cap (default: 10, THB)."),
        ("top [--limit N] [--vs_currency CUR] [--sort-by S]", "Display top N coins with sorting options (default: 10, USD, market_cap)."),
        ("compare <coin1> <coin2>... <vs_currency>", "Compare market data for multiple coins (e.g., compare bitcoin ethereum usd)."),
        ("detail <coin_id>", "Show detailed information for a specific coin (e.g., detail bitcoin)."),
        ("help", "Show this help message.")
    ]
    
    for cmd, desc in commands_info:
        help_text_content.append(f"  {cmd:<40}", style="bold cyan")
        help_text_content.append(f"{desc}\n", style="white")
        
    help_text_content.append("\n👉 Example Usage:\n", style="bold #32CD32")
    help_text_content.append("  python main.py price bitcoin usd\n", style="italic #F0E68C")
    help_text_content.append("  python main.py list --limit 5\n", style="italic #F0E68C")
    help_text_content.append("  python main.py compare bitcoin ethereum solana usd\n", style="italic #F0E68C")
    help_text_content.append("  python main.py top --sort-by volume --vs_currency eur\n", style="italic #F0E68C")
    help_text_content.append("  python main.py detail solana\n", style="italic #F0E68C")

    console.print(Panel(help_text_content, title="[bold #40E0D0]Crypto CLI Help[/]", width=panel_width + 10, border_style="#40E0D0", expand=False))


def main():
    parser = argparse.ArgumentParser(
        description="Crypto CLI - Fetch cryptocurrency data from CoinGecko API.",
        add_help=True
    )

    subparsers = parser.add_subparsers(title="Available Subcommands", help="Run 'main.py <subcommand> -h' for more help on a specific command.", required=True, dest="command_name_for_error")

    # --- Subcommand: price ---
    price_parser = subparsers.add_parser("price", help="Get the current price of a coin.", add_help=True) # เปิด add_help สำหรับ subparser
    price_parser.add_argument("coin_id", type=str, help="The CoinGecko ID of the cryptocurrency (e.g., bitcoin, ethereum).")
    price_parser.add_argument("vs_currency", type=str, help="The currency to compare against (e.g., usd, thb).")
    price_parser.set_defaults(func=handle_price_command)

    # --- Subcommand: list ---
    list_parser = subparsers.add_parser("list", help="List the types of data and features available in this application.", add_help=True)
    list_parser.set_defaults(func=handle_list_command)

    # --- Subcommand: top ---
    top_parser = subparsers.add_parser("top", help="Display top N cryptocurrencies with sorting.", add_help=True)
    top_parser.add_argument("--limit", type=int, default=10, help="Number of top coins to display (default: 10).")
    top_parser.add_argument("--vs_currency", type=str, default="usd", help="The currency for data display (default: usd).") # เปลี่ยนชื่อ help
    top_parser.add_argument("--sort-by", type=str, default="market_cap", choices=['market_cap', 'volume'], help="Sort by 'market_cap' or 'volume' (default: market_cap).")
    top_parser.set_defaults(func=handle_top_command)

    # --- Subcommand: compare ---
    compare_parser = subparsers.add_parser("compare", help="Compare market data for multiple cryptocurrencies.", add_help=True)
    compare_parser.add_argument("coins", nargs="+", help="List of CoinGecko IDs or symbols to compare (e.g., bitcoin ethereum).") 
    compare_parser.add_argument("vs_currency", help="The currency to compare against (e.g., usd, thb).") 
    compare_parser.set_defaults(func=lambda args_obj: handle_compare_command(args_obj, api_key_global=COINGECKO_API_KEY))

    # --- Subcommand: detail ---
    detail_parser = subparsers.add_parser("detail", help="Show detailed information for a specific coin.", add_help=True)
    detail_parser.add_argument("coin_id", type=str, help="CoinGecko ID of the cryptocurrency (e.g., bitcoin).")
    detail_parser.set_defaults(func=handle_detail_command)

    # --- Subcommand: help ---
    help_parser = subparsers.add_parser("help", help="Show this custom help message.", add_help=False) # help ของ help ไม่ต้องมี
    help_parser.set_defaults(func=handle_help_command)
    
    # --- ดักกรณีรัน python main.py โดยไม่ใส่ subcommand ---
    if len(sys.argv) == 1:
        handle_help_command() # เรียก custom help ของเรา
        sys.exit(0) # ออกจากโปรแกรม

    try:
        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            # กรณีนี้ไม่ควรเกิดถ้า subparsers.required=True และทุก command มี func
            # แต่ argparse อาจจะแสดง error ของตัวเองไปแล้ว
            console.print(Panel(Text(f"Error: Subcommand handler not found for '{args.command_name_for_error if hasattr(args, 'command_name_for_error') else 'unknown command'}'.", style="bold red"), title="Internal Error", width=panel_width))
            handle_help_command()
    except argparse.ArgumentError as e: # ดักจับ error จาก argparse โดยเฉพาะ
        console.print(Panel(Text(f"Argument Error: {e}", style="bold red"), title="Input Error", width=panel_width))
        # อาจจะแสดง help ของ subcommand ที่เกี่ยวข้องถ้าทำได้
        # if hasattr(args, 'command_name_for_error') and args.command_name_for_error:
        #    parser.parse_args([args.command_name_for_error, '--help']) # hacky way to show subparser help
        # else:
        handle_help_command() # แสดง custom help หลัก
        sys.exit(1)


if __name__ == "__main__":
    # ตรวจสอบ API Key (นำ comment ออกถ้าต้องการใช้งานจริง)
    if COINGECKO_API_KEY is None:
        console.print(Panel(Text(
            "⚠️ Warning: COINGECKO_API_KEY not found in .env file or environment variables.\n"
            "Some features might not work correctly or might be rate-limited.\n"
            "Please create a .env file with COINGECKO_API_KEY='your_api_key_here'.", style="yellow"
        ), title="API Key Missing", width=panel_width, border_style="yellow"))
        console.print("-" * panel_width)
    main()