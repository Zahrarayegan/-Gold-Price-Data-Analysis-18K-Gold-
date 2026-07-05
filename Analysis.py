import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

pd.options.display.float_format = '{:,.0f}'.format

# -----------------------------
# Read Data
# -----------------------------
df = pd.read_excel(
    "clean_data1.xlsx",
    engine="openpyxl",
    parse_dates=["date_ad"]
)

df = df.sort_values("date_ad")

# -----------------------------
# Daily Return
# -----------------------------
def daily_return(df):

    df = df.copy()

    df["daily_return"] = (
        df["close_price"].pct_change() * 100
    )

    return df


# -----------------------------
# Max Gain / Loss
# -----------------------------
def max_gain_loss(df):

    max_gain = df["daily_return"].max()
    max_loss = df["daily_return"].min()

    print("\n===== بیشترین رشد و ریزش =====")

    print(f"بیشترین رشد روزانه : {max_gain:.2f}%")
    print(f"بیشترین ریزش روزانه : {max_loss:.2f}%")

    return max_gain, max_loss


# -----------------------------
# Volatility
# -----------------------------
def volatility(df):

    df = df.copy()

    df["volatility"] = (
        (df["high_price"] - df["low_price"])
        / df["open_price"]
    ) * 100

    return df


def rolling_volatility(df, window=30):

    df = df.copy()

    df["rolling_volatility"] = (
        df["daily_return"]
        .rolling(window=window)
        .std()
    )

    return df


def show_rolling_volatility(df):

    print("\n========== Rolling Volatility ==========")

    print(
        df[
            [
                "date_ad",
                "daily_return",
                "rolling_volatility"
            ]
        ].tail(30)
    )

# -----------------------------
# Monthly Analysis
# -----------------------------
def monthly_analysis(df):

    result = df.groupby("month").agg({

        "close_price":
        ["mean", "max", "min"],

        "daily_return":
        ["mean", "std"]

    })

    return result


# -----------------------------
# Yearly Analysis
# -----------------------------
def yearly_analysis(df):

    result = df.groupby("year").agg({

        "close_price":
        ["mean", "max", "min"],

        "daily_return":
        ["mean", "std"]

    })

    return result
    
def yearly_mean(df) :
    yearly_mean=df.groupby("year")["close_price"].mean().reset_index()

    return yearly_mean

# -----------------------------
# Statistics
# -----------------------------
def statistics(df):

    print("\n===== آمار قیمت =====")

    print("میانگین قیمت:")
    print(df["close_price"].mean())

    print("میانه قیمت:")
    print(df["close_price"].median())

    print("بیشترین قیمت:")
    print(df["close_price"].max())

    print("کمترین قیمت:")
    print(df["close_price"].min())

    print("انحراف معیار:")
    print(df["close_price"].std())

    print("واریانس:")
    print(df["close_price"].var())

    max_day = df.loc[df["close_price"].idxmax()]
    min_day = df.loc[df["close_price"].idxmin()]

    print("روز بیشترین قیمت:")
    print(max_day["date_ad"])

    print("روز کمترین قیمت:")
    print(min_day["date_ad"])


# -----------------------------
# Moving Average
# -----------------------------
def mean_price(df):

    df = df.copy()

    df["MA7"] = (
        df["close_price"]
        .rolling(7)
        .mean()
    )

    df["MA30"] = (
        df["close_price"]
        .rolling(30)
        .mean()
    )

    df["MA90"] = (
        df["close_price"]
        .rolling(90)
        .mean()
    )

    return df



# -----------------------------
# Chart
# -----------------------------
def chart(df):

    plt.figure(figsize=(15,6))

    plt.plot(
        df["date_ad"],
        df["close_price"],
        label="Close Price"
    )

    plt.plot(
        df["date_ad"],
        df["MA7"],
        label="MA7"
    )

    plt.plot(
        df["date_ad"],
        df["MA30"],
        label="MA30"
    )

    plt.plot(
        df["date_ad"],
        df["MA90"],
        label="MA90"
    )

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.title("18K Gold Price")

    plt.grid(True)

    plt.legend()

    plt.show()

#--------------------
#daily_return_chart
#--------------------

def daily_return_chart(df):

    plt.figure(figsize=(15,5))

    plt.plot(
        df["date_ad"],
        df["daily_return"],
        linewidth=1
    )

    plt.axhline(
        y=0,
        linestyle="--"
    )

    plt.title("Daily Return (%)")

    plt.xlabel("Date")

    plt.ylabel("Return (%)")

    plt.grid(True)

    plt.show()

#----------------
# rolling_volatility_chart
#----------------       

def rolling_volatility_chart(df):

    plt.figure(figsize=(15,6))

    plt.plot(
        df["date_ad"],
        df["rolling_volatility"],
        linewidth=2,
        label="30-Day Rolling Volatility"
    )

    plt.title("30-Day Rolling Volatility")

    plt.xlabel("Date")

    plt.ylabel("Volatility (%)")

    plt.grid(True)

    plt.legend()

    plt.show()

#----------------
# daily_return_histogram
#-----------------

def daily_return_histogram(df):

    plt.figure(figsize=(10,6))

    plt.hist(
        df["daily_return"].dropna(),
        bins=60,
        edgecolor="black"
    )

    plt.axvline(
        x=0,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Zero Return"
    )

    plt.title("Histogram of Daily Returns")

    plt.xlabel("Daily Return (%)")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.legend()

    plt.show()

# ==================================================
# اجرای برنامه
# ==================================================

df = daily_return(df)
df = rolling_volatility(df)
show_rolling_volatility(df)
df = volatility(df)

df = mean_price(df)


statistics(df)

max_gain_loss(df)

monthly_result = monthly_analysis(df)

yearly_result = yearly_analysis(df)

yearly_mean = yearly_mean(df)

print("\n===== تحلیل ماهانه =====")
print(monthly_result)

print("\n===== تحلیل سالانه =====")
print(yearly_result)

print("\n===== 5 سطر اول =====")
print(df.head())


chart(df)
daily_return_chart(df)
rolling_volatility_chart(df)
daily_return_histogram(df)
yearly_average_bar(df)
