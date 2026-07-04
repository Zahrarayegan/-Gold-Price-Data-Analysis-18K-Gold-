from numpy import float64, int64
import pandas as pd
import parquet
import openpyxl
file = pd.read_excel("tgju_gold18_history.xlsx")


def clean_data():
    cols = [
        'low_price',
        'high_price',
        'close_price',
        'open_price',
        
    ]

    for col in cols:
        file[col] = file[col].str.replace(',', '', regex=False).astype('int64')

    
    file['change_amount'] = file['change_amount'].replace('-', '0').astype('int64')
    file['change_percent'] = file['change_percent'].replace('-', '0').str.replace('%', '', regex=False).astype('float64')
    file['date_ad'] = pd.to_datetime(file['date_ad']).astype('datetime64[ns]')
    file["year"] = file["date_ad"].dt.year

    file["month"] = file["date_ad"].dt.month
    return file

df = clean_data()
""" Cleaned_Data = df.to_csv("Cleaned_Data.csv", index=False)
Cleaned_Data = df.to_excel("clean_data1.xlsx", index=False)

if Cleaned_Data:
        Cleaned_Data = df.to_excel("Cleaned_Data.xlsx", index=False)
        print("فایل ها با موفقیت ذخیره شدند.") """


    
            
#df.to_parquet("Cleaned_Data.parquet")
#print(df.head())
#print(df.tail())
print(df.info())