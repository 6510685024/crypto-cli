# 🗂️ Crypto-CLI

> **Crypto-CLI** เป็นแอปพลิเคชันแบบ Command Line Interface (CLI) สำหรับเรียกดูข้อมูลเกี่ยวกับเหรียญคริปโต โดยใช้ข้อมูลจาก CoinGecko API  
> เหมาะสำหรับนักพัฒนาหรือผู้สนใจคริปโตที่ต้องการติดตามข้อมูลเหรียญผ่านเทอร์มินัล


## 🌟 คุณสมบัติหลัก

🔹 คำสั่งที่สามารถใช้งานได้:

- `help` – แสดงรายการคำสั่งทั้งหมด
- `list` – แสดงชนิดข้อมูลและฟีเจอร์
- `price` – แสดงราคาของเหรียญในสกุลเงินที่ต้องการ
- `compare` – เปรียบเทียบราคาของหลายเหรียญ
- `top` – แสดงเหรียญอันดับสูงสุดตาม market cap หรือ volume
- `detail` – แสดงรายละเอียดเชิงลึกของเหรียญ


## 👥 ทีมผู้พัฒนา [Team 1]
- **Jakapat Sombatcharoenmuang** (`6510685024`)
- **Kanchana Duangcharee** (`6510615013`)
- **Nalinporn Promphen** (`6410685017`)
- **Kitipat Malisorn** (`6310540015`)


## 🛠️ วิธีการติดตั้งและใช้งาน

### 🚀 วิธีที่ 1: ใช้งานด้วย Python (Virtual Environment)

1. **Clone repository:**
   ```bash
   git clone https://github.com/6510685024/crypto-cli.git
   cd crypto-cli
   ```

2. **สร้าง Virtual Environment:**
   ```bash
   python3 -m venv venv
   ```

3. **เปิดใช้งาน Virtual Environment:**
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **ติดตั้ง dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **ใช้งานคำสั่ง:**
   ```bash
   python main.py <command> [arguments]
   ```


### 🐳 วิธีที่ 2: ใช้งานผ่าน Docker

#### 🔹 แบบไม่ใช้ `.env`

1. **Build และ Run container:**
   ```bash
   docker build -t crypto-cli .
   docker run -it crypto-cli <command> [arguments]
   ```

2. **ตัวอย่าง:**
   ```bash
   docker run -it crypto-cli price bitcoin usd
   docker run -it crypto-cli list
   ```

#### 🔹 แบบใช้ `.env` (กรณีมี API Key)

1. **สร้างไฟล์ `.env`:**
   ```env
   COINGECKO_API_KEY=your_api_key
   ```

    หมายเหตุ: สามารถศึกษาการขอ API KEY ได้จาก https://docs.coingecko.com/reference/setting-up-your-api-key
2. **Mount ไฟล์ `.env` และรัน:**
   ```bash
   docker run --env-file .env -it crypto-cli <command> [arguments]
   ```

3. **ตัวอย่าง:**
   ```bash
   docker run --env-file .env -it crypto-cli price bitcoin usd
   docker run --env-file .env -it crypto-cli top --limit 5 --vs_currency eur
   ```


### 📦 วิธีที่ 3: ใช้งานผ่าน Docker Compose

1. **Build และ Run ด้วย Compose:**
   ```bash
   docker compose build
   docker compose up
   ```

2. **รันคำสั่งภายใน container:**
   ```bash
   docker compose run app <command> [arguments]
   ```


## 📘 ตัวอย่างคำสั่งที่ใช้งานได้

### 🔹 `price`

แสดงราคาของเหรียญในสกุลเงินที่กำหนด

```bash
python main.py price <coin_id> <vs_currency>
```

📍 *ตัวอย่าง:* แสดงราคา Bitcoin เป็น USD
```bash
python main.py price bitcoin usd
```


### 🔹 `list`

แสดงข้อมูลชนิดเหรียญและฟีเจอร์ที่รองรับ

```bash
python main.py list
```


### 🔹 `compare`

เปรียบเทียบราคาของหลายเหรียญในสกุลเงินที่ระบุ

```bash
python main.py compare <coin1> <coin2> ... <vs_currency>
```

📍 *ตัวอย่าง:* เปรียบเทียบราคาของ Bitcoin, Ethereum, Solana เป็น USD
```bash
python main.py compare bitcoin ethereum solana usd
```


### 🔹 `top`

แสดงอันดับเหรียญสูงสุดตาม Market Cap หรือ Volume

```bash
python main.py top [--limit N] [--vs_currency CUR] [--sort-by S]
```

- `--limit`: จำนวนเหรียญ (ค่าเริ่มต้น: 10)
- `--vs_currency`: สกุลเงินที่ต้องการ (ค่าเริ่มต้น: usd)
- `--sort-by`: `market_cap` (default) หรือ `volume`

📍 *ตัวอย่าง:* แสดง 10 อันดับเหรียญตาม market cap
```bash
python main.py top
```

📍 *ตัวอย่าง:* แสดง 5 อันดับเหรียญตาม volume ในสกุล EUR
```bash
python main.py top --limit 5 --sort-by volume --vs_currency eur
```


### 🔹 `detail`

แสดงรายละเอียดเชิงลึกของเหรียญ

```bash
python main.py detail <coin_id>
```

📍 *ตัวอย่าง:* แสดงข้อมูลของ Solana
```bash
python main.py detail solana
```


## 🪙 ตัวอย่างเหรียญที่รองรับ

| ชื่อเหรียญ | coin_id ที่ใช้ |
|------------|----------------|
| Bitcoin    | `bitcoin`      |
| Ethereum   | `ethereum`     |
| Solana     | `solana`       |
| Dogecoin   | `dogecoin`     |
| Cardano    | `cardano`      |


## ⚠️ หมายเหตุเพิ่มเติม

- หากใช้ `.env` ต้องระบุ `COINGECKO_API_KEY` ให้ถูกต้อง