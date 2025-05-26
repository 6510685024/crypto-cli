import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt 
from babel.numbers import get_currency_symbol 
from rich import box

console = Console()

def fetch_coin_id_map():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        symbol_to_ids = {}
        name_to_id = {}

        for coin in data:
            coin_id = coin["id"]
            symbol = coin["symbol"].lower()
            name = coin["name"].lower()

            name_to_id[name] = coin_id

            if symbol not in symbol_to_ids:
                symbol_to_ids[symbol] = []
            symbol_to_ids[symbol].append(coin_id)

        return symbol_to_ids, name_to_id

    except requests.exceptions.RequestException as e:
        console.print(f"[bold #df0000]❌ Failed to fetch coin list from CoinGecko:[/bold #df0000] {e}")
        return {}, {}

def resolve_coin_ids(user_inputs, symbol_to_ids, name_to_id):
    resolved_ids = []
    not_found = []

    for raw in user_inputs:
        key = raw.lower()

        if key in name_to_id:
            resolved_ids.append(name_to_id[key])

        elif key in symbol_to_ids:
            candidates = symbol_to_ids[key]
                
            if len(candidates) == 1:
                resolved_ids.append(candidates[0])
            else:
                console.print(f"\n[bold #f6e10d]🔎 Found multiple coins with symbol '{key}':[/bold #f6e10d]")
                for idx, cid in enumerate(candidates, start=1):
                    console.print(f"  [cyan]{idx}[/cyan]: {cid}")

                try:
                    choice = Prompt.ask(
                        f"[bold #f9730a]Select number (1-{len(candidates)}) for '{key}' coin you are looking for[/bold #f9730a]" 
                    )
                    resolved_ids.append(candidates[int(choice) - 1])
                except Exception:
                    console.print("[#df0000]⚠️ Skipped due to invalid input[/#df0000]")
        else:
            not_found.append(raw)

    if not_found:
        console.print(f"\n[bold #df0000]❌ Could not identify:[/bold #df0000] {', '.join(not_found)}")
        console.print("   [bold #df0000]Please try using full coin name or valid symbol[/bold #df0000]")

    return list(dict.fromkeys(resolved_ids))  # Remove duplicates coin

def handle_compare_command(args):
    user_inputs = args.coins
    vs_currency = args.vs_currency

    symbol_to_ids, name_to_id = fetch_coin_id_map()
    coin_ids = resolve_coin_ids(user_inputs, symbol_to_ids, name_to_id)

    if not coin_ids:
        console.print("[bold #df0000]❌ No valid coins to compare.[/bold #df0000]")
        return

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "ids": ','.join(coin_ids),
        "vs_currency": vs_currency,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            console.print("[#df0000]⚠️ Coin information not found from CoinGecko[/#df0000]")
            return

        currency_symbol = get_currency_symbol(vs_currency.upper(), locale="en_US")
        
        table = Table(
            title="📊 Cryptocurrency Price Comparison",
            box=box.ROUNDED,
            #show_lines=True,               
            border_style="#ea137b",           
            style="white",                
        )

        table.add_column("Coin", style="bold cyan")
        table.add_column("Price", justify="right", style="green")
        table.add_column("Market Cap", justify="right", style="#ffb731")
        table.add_column("Volume (24h)", justify="right", style="magenta")
        table.add_column("Change (24h)%", justify="right", style="#ed2121")

        for coin in data:
            name = coin.get('name', 'N/A')
            price = f"{currency_symbol}{coin.get('current_price', 0):,.2f}"
            market_cap = f"{currency_symbol}{coin.get('market_cap', 0):,.0f}"
            volume = f"{currency_symbol}{coin.get('total_volume', 0):,.0f}"
            change = f"{coin.get('price_change_percentage_24h', 0):,.2f}%"
            
            table.add_row(name, price, market_cap, volume, change)

        console.print("\n", table, "\n")
        
    except requests.exceptions.RequestException as e:
        console.print(f"[bold #df0000]❌ Error fetching data from CoinGecko:[/bold #df0000] {e}")
