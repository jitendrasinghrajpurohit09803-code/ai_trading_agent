import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# पेज सेटअप
st.set_page_config(page_title="Jitendra AI Trading", layout="wide")
st.title("📈 Jitendra Singh's AI Trading Agent")

# साइडबार में इनपुट
symbol = st.sidebar.text_input("शेयर का नाम लिखें (जैसे: RELIANCE.NS)", value="NIFTY50.NS")

if symbol:
    try:
        # डेटा डाउनलोड करना
        data = yf.download(symbol, period="5d", interval="15m")
        
        if not data.empty:
            # वर्तमान कीमत (Last Price)
            last_price = float(data['Close'].iloc[-1])
            st.metric(label=f"{symbol} की वर्तमान कीमत", value=f"₹{last_price:.2f}")
            
            # कैंडलस्टिक चार्ट बनाना
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                            open=data['Open'], high=data['High'],
                            low=data['Low'], close=data['Close'])])
            
            fig.update_layout(title=f"{symbol} लाइव चार्ट", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success("AI एजेंट सफलतापूर्वक डेटा स्कैन कर रहा है!")
        else:
            st.error("डेटा नहीं मिला। कृपया सही सिंबल डालें।")
    except Exception as e:
        st.error(f"कुछ तकनीकी समस्या आई: {e}")
