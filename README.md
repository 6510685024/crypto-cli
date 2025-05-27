# crypto-cli


## สมาชิก

**Team 1**
***
1.  Jakapat Sombatcharoenmuang (`6510685024`)
2.  Kanchana Duangcharee (`6510615013`)
3.  Nalinporn Promphen (`6410685017`)
4.  Kitipat Malisorn (`6310540015`)

## วิธีการรัน

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/6510685024/crypto-cli.git](https://github.com/6510685024/crypto-cli.git)
    cd crypto-cli
    ```

2.  **สร้าง Virtual Environment:**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate Virtual Environment:**
    * **macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        venv/Scripts/activate
        ```

4.  **ติดตั้ง Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install python-dotenv
    ```

5.  **เลือก Branch:**
    ```bash
    git checkout main
    ```

6.  **Build และ Run Docker Compose:**
    ```bash
    docker compose build
    docker compose up
    ```

    > หากพบข้อผิดพลาดเกี่ยวกับ Module ที่ไม่ครบถ้วน ให้ติดตั้ง Module นั้นๆ ด้วยคำสั่ง `pip install <ชื่อ module>`

## การใช้งานคำสั่ง

### Price

แสดงราคาของเหรียญคริปโตที่ระบุในสกุลเงินที่ต้องการ
```bash
python main.py price <coin_id> <vs_currency>
```

**ตัวอย่าง:** แสดงราคา Bitcoin ในสกุล USD
```bash
python main.py price bitcoin usd
```

### List

**ตัวอย่าง:** แสดงประเภทการทำงาน
```bash
python main.py list
```

### Compare
เปรียบเทียบข้อมูลราคาของเหรียญคริปโตหลายเหรียญในสกุลเงินที่ต้องการ
```bash
python main.py compare <coin1> <coin2>... <vs_currency>
```

**ตัวอย่าง:** แสดงการเปรียบเทียบราคาเหรียญคริปโต อย่าง bitcoin, ethereum, solana ในสกุล USD
```bash
python main.py compare bitcoin ethereum solana usd
```

### Top
แสดงรายการเหรียญคริปโตตามอันดับ โดยมีตัวเลือกในการจำกัดจำนวน, สกุลเงิน, และวิธีการเรียงลำดับ

```bash
python main.py top [--limit N] [--vs_currency CUR] [--sort-by S]
```
ตัวเลือก --sort-by: เลือกจาก 'market_cap', 'volume'

**ตัวอย่าง:** แสดงเหรียญคริปโต 10 อันดับแรก โดยเรียงตาม market cap (ค่าเริ่มต้น) และแสดงราคาในสกุล USD (ค่าเริ่มต้น)
```bash
python main.py top
```

**ตัวอย่าง:** แสดงเหรียญคริปโต 5 อันดับแรก โดยเรียงตาม volume และแสดงราคาในสกุล EUR
```bash
python main.py top --limit 5 --sort-by volume --vs_currency eur
```

### Detail
แสดงรายละเอียดของเหรียญคริปโตที่ระบุ
```bash
python main.py detail <coin_id>
```

**ตัวอย่าง:** แสดงรายละเอียดของ Solana
```bash
python main.py detail solana
```