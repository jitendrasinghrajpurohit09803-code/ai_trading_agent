import yfinance as yf
import pyttsx3
import time
import requests
import pandas as pd

# Voice Setup
engine = pyttsx3.init()
engine.setProperty('rate', 150) # आवाज़ की गति थोड़ी कम करने के लिए

def speak(text):
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()

# Telegram Bot Setup
# अपना असली टोकन यहाँ डालें
TOKEN = "8777198835:AAGBRV9b6_oXrKIugUH0_Tpl7uT6UtCLVMc" 
CHAT_ID = "123456789" # अपना टेलीग्राम चैट आईडी यहाँ लिखें

def send_alert(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print(f"Telegram Error: {e}")

# Trading Analysis (RSI)
def analyze():
    # NIFTY 50 (^NSEI) का डेटा ले रहे हैं
    data = yf.download("^NSEI", period="2d", interval="5m", progress=False)

    if len(data) < 14:
        return "Waiting for more market data..."

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    current_rsi = rsi.iloc[-1]
    
    if current_rsi < 30:
        return f"BUY Signal 📈 (RSI is {current_rsi:.2f})"
    elif current_rsi > 70:
        return f"SELL Signal 📉 (RSI is {current_rsi:.2f})"
    else:
        return f"Market is Neutral (RSI: {current_rsi:.2f})"

# Main Loop
print("AI Trading Agent Started...")
while True:
    try:
        signal = analyze()
        speak(signal)
        # सिर्फ सिग्नल होने पर टेलीग्राम अलर्ट भेजें
        if "Signal" in signal:
            send_alert(signal)
    except Exception as e:
        print(f"Error: {e}")
    
    # 5 मिनट इंतज़ार (क्योंकि डेटा 5m इंटरवल का है)
    time.sleep(300)