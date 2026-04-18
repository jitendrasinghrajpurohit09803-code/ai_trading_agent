import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import requests
import io
from gtts import gTTS

# --- कॉन्फ़िगरेशन (अपनी डिटेल्स यहाँ भरें) ---
TOKEN = "8777198835:AAGBRV9b6_oXrKIugUH0_Tpl7uT6UtCLVMc"
CHAT_ID = "5053420281"
# पेज सेटअप
st.set_page_config(page_title="Jitendra AI Agent", layout="wide")
st.title("🤖 Jitendra's AI Trading Dashboard")

# टेलीग्राम पर वॉइस मैसेज भेजने वाला फंक्शन
def send_voice_alert(text):
    try:
        tts = gTTS(text=text, lang='hi')
        voice_file = io.BytesIO()
        tts.write_to_fp(voice_file)
        voice_file.seek(0)
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendVoice"
        files = {'voice': ('alert.ogg', voice_file, 'audio/ogg')}
        requests.post(url, data={'chat_id': CHAT_ID}, files=files)
    except Exception as e:
        st.error(f"Telegram Alert Error: {e}")

# साइडबार ऑप्शंस
st.sidebar.header("Settings")
target_stock = st.sidebar.selectbox("Stock सिलेक्ट करें", ["^NSEI", "RELIANCE.NS", "SBIN.NS", "TCS.NS", "TATAMOTORS.NS"])
time_interval = st.sidebar.selectbox("Time Interval", ["5m", "15m", "1h"])

# डेटा लोड करना
data = yf.download(target_stock, period="2d", interval=time_interval)

if not data.empty:
    # इंडिकेटर्स (RSI और EMA)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    
    last_price = float(data['Close'].iloc[-1])
    last_rsi = float(data['RSI'].iloc[-1])
    avg_vol = data['Volume'].tail(20).mean()
    curr_vol = data['Volume'].iloc[-1]

    # डैशबोर्ड मेट्रिक्स
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"₹{last_price:.2f}")
    col2.metric("RSI (14)", f"{last_rsi:.2f}")
    
    # सिग्नल लॉजिक
    signal = "Neutral"
    if last_rsi < 35 and curr_vol > (avg_vol * 1.2):
        signal = "🚀 STRONG BUY"
        msg = f"जीतेन्द्र जी, {target_stock} में खरीदने का संकेत है। RSI कम है और वॉल्यूम बढ़ रहा है।"
        send_voice_alert(msg)
        st.success(msg)
    elif last_rsi > 65 and curr_vol > (avg_vol * 1.2):
        signal = "⚠️ STRONG SELL"
        msg = f"जीतेन्द्र जी, {target_stock} में बेचने का समय हो सकता है। RSI काफी ऊपर है।"
        send_voice_alert(msg)
        st.error(msg)
    
    col3.metric("Current Signal", signal)

    # चार्ट बनाना
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'], name="Market Data")])
    
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name="EMA 20", line=dict(color='orange')))
    
    fig.update_layout(title=f"{target_stock} Live Chart", yaxis_title="Price", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("डेटा लोड नहीं हो सका। कृपया मार्केट खुलने का इंतज़ार करें या स्टॉक बदलें।")
