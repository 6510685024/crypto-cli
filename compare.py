import requests

def fetch_coin_id_map(): # ดึงเหรียญมา map ไว้
    
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

            # mapping ชื่อเต็ม → id
            name_to_id[name] = coin_id

            # symbol → list of ids
            if symbol not in symbol_to_ids:
                symbol_to_ids[symbol] = []
            symbol_to_ids[symbol].append(coin_id)

        return symbol_to_ids, name_to_id

    except requests.exceptions.RequestException as e:
        print("Failed to fetch coin list from CoinGecko:", e)
        return {}, {}

def resolve_coin_ids(user_inputs, symbol_to_ids, name_to_id):
    """
    แปลง input ของผู้ใช้ (symbol/full name) → coin IDs 
    ถ้าพบ symbol ที่มีหลายเหรียญ ถาม user เพื่อเลือก
    """
    resolved_ids = []
    not_found = []

    for raw in user_inputs:
        key = raw.lower()

        # ถ้า user พิมพ์ชื่อเต็ม
        if key in name_to_id:
            resolved_ids.append(name_to_id[key])

        # ถ้า user พิมพ์ symbol
        elif key in symbol_to_ids:
            candidates = symbol_to_ids[key]

            # ถาม user ให้เลือก เพราะบาง symbol map หลาย coin
            print(f"\n🔎 Found many coin with symbol '{key}':")
            for idx, cid in enumerate(candidates, start=1):
                print(f"  [{idx}] {cid}")

            try:
                choice = int(input(f"select number (1-{len(candidates)}) for '{key}' coin you are looking for: "))
                if 1 <= choice <= len(candidates):
                    resolved_ids.append(candidates[choice - 1])
                else:
                    print("Skip this coin because the number was not entered")
            except ValueError:
                print("Skip this coin because the number was not entered")
       
        else:
            not_found.append(raw)

    if not_found:
        print(f"\nThe following coins could not be identified: {', '.join(not_found)}")
        print("   Please try using a valid full name or a valid symbol")

    # ลบเหรียญซ้ำ 
    return list(dict.fromkeys(resolved_ids))

def handle_compare_command(args):
    user_inputs = args.coins
    vs_currency = args.vs_currency

    # ดึงข้อมูล mapping จาก CoinGecko
    symbol_to_ids, name_to_id = fetch_coin_id_map()
    coin_ids = resolve_coin_ids(user_inputs, symbol_to_ids, name_to_id)

    if not coin_ids:
        print("There is no coin that can compare.")
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
            print("Coin information not found from CoinGecko")
            return
        
        print(f"\n{'Coin':20} {'Price':>15} {'Market Cap':>20} {'Volume (24h)':>20} {'Change (24h)%':>18}")
        print("-" * 100)

        for coin in data:
            name = coin.get('name', 'N/A')
            price = coin.get('current_price', 0)
            market_cap = coin.get('market_cap', 0)
            volume = coin.get('total_volume', 0)
            change = coin.get('price_change_percentage_24h', 0)

            print(f"{name:20} {price:>15,.2f} {market_cap:>20,.0f} {volume:>20,.0f} {change:>18,.2f}")
        print("\n")
            
    except requests.exceptions.RequestException as e:
        print("Error fetching data from CoinGecko:", e)