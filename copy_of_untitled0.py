import streamlit as st
import yfinance as yf

stock_list = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "LT.NS", "KOTAKBANK.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "SUNPHARMA.NS",
    "HCLTECH.NS", "AXISBANK.NS", "MARUTI.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

st.title("📈 AI Stock Signal Screener")

action = st.selectbox("Choose Signal Type:", ["Buy (Bullish)", "Sell (Bearish)"])

def analyze_stock(symbol):
    try:
        data = yf.download(symbol, period="1d", interval="5m", progress=False)
        if data.empty:
            return None
        close = data["Close"]
        trend = "bullish" if close[-1] > close[-3] else "bearish"
        price = close[-1]
        time = close.index[-1].strftime("%H:%M")
        return (symbol, price, time, trend)
    except:
        return None

if st.button("📈 Get Today's Top Picks"):
    results = []
    for stock in stock_list:
        st.write(f"Checking {stock}...")
        result = analyze_stock(stock)
        if result:
            symbol, price, time, trend = result
            if ("Buy" in action and trend == "bullish") or ("Sell" in action and trend == "bearish"):
                results.append(result)
        if len(results) >= 5:
            break

    if results:
        st.subheader(f"🔍 Top {action} Picks")
        for symbol, price, time, trend in results:
            st.write(f"*{symbol}* → ₹{price:.2f} at {time} ({trend})")
    else:
        st.warning("⚠️ No strong signals right now.")