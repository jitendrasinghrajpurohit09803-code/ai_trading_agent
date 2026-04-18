import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="Jitendra AI Trading Agent", layout="wide")
st.title("📈 Jitendra's AI Trading Dashboard")

symbol = st.sidebar.text_input("Enter Stock Symbol (e.g. RELIANCE.NS)", value="NIFTY50.NS")

if symbol:
    data = yf.download(symbol, period="1d", interval="15m")
    if not data.empty:
        # यहाँ हमने स्पेस (Indentation) सही कर दिया है
        last_price = float(data['Close'].iloc[-1])
        st.metric(label=f"Current Price of {symbol}", value=f"₹{last_price:.2f}")
        
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No data found. Please check the symbol.")
