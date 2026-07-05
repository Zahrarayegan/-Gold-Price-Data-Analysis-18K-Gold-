import requests 
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook

url =("https://api.tgju.org/v1/market/indicator/summary-table-data/geram18?lang=fa&order_dir=asc&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=30&search=&order_col=&order_dir=&from=&to=&convert_to_ad=1&_=1781457989127"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

def clean_html(text):
    

    return BeautifulSoup(str(text), "html.parser").get_text(strip=True)
all_rows = []
start = 0
length = 30

while True:
    param = {
        'lang': 'fa',
        'start': start,
        'length': length,
        'convert_to_ad': 1
          }
    try:
        r = requests.get(url, params=param, headers=headers,timeout=30)
        data = r.json()
        rows = data.get('data', [])
        if not rows:
            print("No more data to download.")
            break
        all_rows.extend(rows)        
    
        print(
            f"صفحه {(start // length) + 1} | "
            f"دریافت {len(rows)} رکورد | "
            f"مجموع: {len(all_rows)}"
        )
        start += length

        time.sleep(0.5)
    except Exception as e:
        print(f"خطا در دریافت داده: {e}")
        break    
print(f"\nتعداد کل رکوردها: {len(all_rows)}")

cleaned_rows = []

for row in all_rows:

    cleaned_row = []

    for cell in row:
        cleaned_row.append(clean_html(cell))

    cleaned_rows.append(cleaned_row)

if not cleaned_rows:
    print("هیچ داده‌ای دریافت نشد.")
    exit()
# اگر تعداد ستون ها متفاوت بود
max_cols = max(len(r) for r in cleaned_rows)

columns = [f"col_{i+1}" for i in range(max_cols)]

df = pd.DataFrame(cleaned_rows, columns=columns)
df = df.map(clean_html)
df.columns = [
    "open_price",
    "low_price",
    "high_price",
    "close_price",
    "change_amount",
    "change_percent",
    "date_ad",
    "date_shamsi"
]

print("\nنمونه داده:")

print(df.head())


# ذخیره CSV
df.to_csv(
    "tgju_gold18_history.csv",
    index=False,
    encoding="utf-8-sig"
)

# ذخیره Excel
df.to_excel(
    "tgju_gold18_history.xlsx",
    index=False
)

print("\nفایل ها ذخیره شدند:")
print("tgju_gold18_history.csv")
print("tgju_gold18_history.xlsx")

