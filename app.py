import streamlit as st
import requests
import time
from streamlit_autorefresh import st_autorefresh

# Streamlit Page configuration
st.set_config = st.set_page_config(page_title="Binance Luxury Scanner", layout="wide")

# ১ ঘণ্টা (৩৬০০ সেকেন্ড) পর পর অটোমেটিক পেজ রিফ্রেশ ও স্ক্যান করার জন্য অটো-রিফ্রেশার
st_autorefresh(interval=3600 * 1000, key="binance_scanner_refresh")

# টেলিগ্রাম কনফিগারেশন
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# বিন্যান্স স্টাইলে কয়েন লিস্ট (USDT Pair)
binance_symbols = [
    # ১. মেগা ও লার্জ ক্যাপ অল্টকয়েন
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
    "ADAUSDT", "DOTUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", 
    "DOGEUSDT", "SHIBUSDT", "MATICUSDT", "ATOMUSDT", "BCHUSDT", 
    "ETCUSDT", "XLMUSDT", "NEARUSDT", "TRXUSDT", "UNIUSDT",

    # ২. লেয়ার ১ এবং লেয়ার ২ ইকোসিস্টেম
    "SUIUSDT", "APTUSDT", "TONUSDT", "INJUSDT", "SEIUSDT", 
    "FTMUSDT", "ALGOUSDT", "EGLDUSDT", "TIAUSDT", "MINAUSDT", 
    "FLOWUSDT", "ICPUSDT", "EOSUSDT", "KAVAUSDT", "ASTRUSDT", 
    "ONEUSDT", "HBARUSDT", "IOTAUSDT", "NEOUSDT", "QTUMUSDT", 
    "VETUSDT", "ZILUSDT", "WAVESUSDT", "THETAUSDT", "STRAXUSDT",
    "ARBUSDT", "OPUSDT", "STRKUSDT", "METISUSDT", "MANTAUSDT", 
    "SKLUSDT", "CELOUSDT", "LRCUSDT", "IMXUSDT", "OMGUSDT", "ROSEUSDT",

    # ৩. মিম কয়েন
    "PEPEUSDT", "WIFUSDT", "BONKUSDT", "FLOKIUSDT", "BOMEUSDT", 
    "MEMEUSDT", "MYROUSDT", "1000SATSUSDT", "TURBOUSDT", "BABYDOGEUSDT", 
    "PEOPLEUSDT", "WENUSDT", "AIDOGEUSDT", "1000RATSUSDT", "NOTUSDT", 
    "POPCATUSDT", "MEWUSDT", "BRETTUSDT", "MOGUSDT", "NEIROUSDT", 
    "MOODENGUSDT", "GOATUSDT", "PNUTUSDT", "ACTUSDT", "FBUSDT", 
    "SUNDOGUSDT", "CHILLGUYUSDT",

    # ৪. AI, DePIN এবং বিগ ডেটা
    "FETUSDT", "RNDRUSDT", "GRTUSDT", "TAOUSDT", "AKTUSDT", 
    "AGIXUSDT", "OCEANUSDT", "PHBUSDT", "ARKMUSDT", "WLDUSDT", 
    "NFPUSDT", "AIUSDT", "LPTUSDT", "FILUSDT", "ARUSDT", 
    "JASMYUSDT", "STORJUSDT", "BLZUSDT", "ANKRUSDT", "IONETUSDT", 
    "NOSUSDT", "CLOREUSDT", "GLMUSDT", "ORDIUSDT", "MDTUSDT", 
    "CTXCUSDT", "IQUSDT", "GTCUSDT", "CLVUSDT",

    # ৫. ডেফি, আরডব্লিউএ এবং ওয়েব৩ প্রজেক্টস
    "AAVEUSDT", "PENDLEUSDT", "MKRUSDT", "CRVUSDT", "LDOUSDT", 
    "JUPUSDT", "RUNEUSDT", "DYDXUSDT", "ENSUSDT", "COMPUSDT", 
    "SNXUSDT", "SUSHIUSDT", "YFIUSDT", "CAKEUSDT", "BAKEUSDT", 
    "RAYUSDT", "JOEUSDT", "JTOUSDT", "ORCAUSDT", "COWUSDT", 
    "1INCHUSDT", "BALUSDT", "BADGERUSDT", "ALPHAUSDT", "ENAUSDT", 
    "DRIFTUSDT", "SAFEUSDT", "PYTHUSDT", "AXLUSDT", "ONDOUSDT", 
    "TRUUSDT", "ALPACAUSDT", "BELUSDT", "AUCTIONUSDT", "TROYUSDT", 
    "QUICKUSDT", "FISUSDT", "UNFIUSDT", "ETHFIUSDT", "REZUSDT", 
    "OMNIUSDT", "TNSRUSDT", "SAGAUSDT", "BBUSDT", "DNTUSDT", 
    "WRXUSDT", "SCRUSDT", "HYPEUSDT", "VTHOUSDT", "CELRUSDT", 
    "COMBOUSDT", "CETUSUSDT",

    # ৬. গেমিং এবং মেটাভার্স (GameFi)
    "GALAUSDT", "AXSUSDT", "SANDUSDT", "MANAUSDT", "PIXELUSDT", 
    "BEAMXUSDT", "YGGUSDT", "ILVUSDT", "ALICEUSDT", "ENJUSDT", 
    "MAGICUSDT", "PORTALUSDT", "XAIUSDT", "CHZUSDT", "SUPERUSDT", 
    "VOXELUSDT", "DARUSDT", "TLMUSDT", "BIGTIMEUSDT", "TOKENUSDT", 
    "VANRYUSDT", "MBOXUSDT", "HIGHUSDT",

    # ৭. ইনফ্রাস্ট্রাকচার ও ক্রস-চেইন (Oracle)
    "WUSDT", "STGUSDT", "SYNUSDT", "GLMRUSDT", "MOVRUSDT", 
    "KSMUSDT", "ICXUSDT", "BANDUSDT", "TRBUSDT", "DIAUSDT",

    # ৮. ওল্ড-স্কুল অল্টকয়েন ও ট্রেন্ডিং লো-ক্যাপ
    "ZECUSDT", "XMRUSDT", "DASHUSDT", "ZENUSDT", "ONTUSDT", 
    "IOTXUSDT", "RVNUSDT", "HOTUSDT", "BATUSDT", "KNCUSDT", 
    "ZRXUSDT", "RENUSDT", "WOOUSDT", "GMTUSDT", "IDUSDT", 
    "EDUUSDT", "HOOKUSDT", "CYBERUSDT", "MAVUSDT", "ARKUSDT", 
    "POLYUSDT", "LOOMUSDT", "BONDUSDT", "VGXUSDT", "RADUSDT"
]

# --- UI Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f8fafc;
    }
    h1 {
        color: #00d2ff !important;
        background: linear-gradient(to right, #00ffff, #0088ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.3);
    }
    .scanning-box {
        background: rgba(17, 24, 39, 0.85);
        border: 2px solid #38bdf8;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 1.5s infinite alternate;
    }
    .scanning-coin {
        font-size: 3rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
    }
    @keyframes pulse {
        0% { transform: scale(0.99); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        100% { transform: scale(1.01); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }
    }
    .signal-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        font-family: monospace;
    }
    .buy-card {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
    }
    .sell-card {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #ef4444;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Luxury Binance Auto-Scanner (H1 Frame)")
st.write("বাইন্যান্স এপিআই চালিত ১ ঘণ্টার স্বাধীন অটো-স্ক্যানার। প্রতি ১ ঘণ্টা পর পর সচল হবে।")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

# কাস্টম টেকনিক্যাল ইন্ডিকেটর (Pandas ছাড়া)
def calculate_ema(prices, period=200):
    if len(prices) < period:
        return [0] * len(prices)
    ema = []
    k = 2 / (period + 1)
    sma = sum(prices[:period]) / period
    ema.append(sma)
    for price in prices[period:]:
        next_ema = (price * k) + (ema[-1] * (1 - k))
        ema.append(next_ema)
    return [0] * (period - 1) + ema

def calculate_macd(prices, slow=26, fast=12, signal_period=9):
    if len(prices) < slow:
        return [], []
    k_fast = 2 / (fast + 1)
    ema_fast = [prices[0]]
    for p in prices[1:]:
        ema_fast.append((p * k_fast) + (ema_fast[-1] * (1 - k_fast)))
    k_slow = 2 / (slow + 1)
    ema_slow = [prices[0]]
    for p in prices[1:]:
        ema_slow.append((p * k_slow) + (ema_slow[-1] * (1 - k_slow)))
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    if len(macd_line) < signal_period:
        return [], []
    k_sig = 2 / (signal_period + 1)
    signal_line = [macd_line[0]]
    for m in macd_line[1:]:
        signal_line.append((m * k_sig) + (signal_line[-1] * (1 - k_sig)))
    return macd_line, signal_line

# বিন্যান্স স্পট এপিআই দিয়ে ডাটা অ্যানালাইসিস
def fetch_and_analyze_binance(symbol):
    # Binance Klines API (1h Timeframe) - ৩০০টি ক্যান্ডেল নিয়ে আসা হচ্ছে
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=300"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        if len(data) < 220:
            return None
        
        # বিন্যান্স ক্যান্ডেল ফরম্যাট: [OpenTime, Open, High, Low, Close, ...]
        highs = [float(candle[2]) for candle in data]
        lows = [float(candle[3]) for candle in data]
        closes = [float(candle[4]) for candle in data]
        
        current_close = closes[-1]
        
        # ১. 200 EMA
        ema200_list = calculate_ema(closes, 200)
        current_ema200 = ema200_list[-1]
        
        # ২. MACD Divergence Lookback=30
        macd_line, signal_line = calculate_macd(closes)
        if not macd_line or not signal_line:
            return None
        m_lookback = macd_line[-30:]
        
        macd_divergence_bullish = False
        macd_divergence_bearish = False
        if len(m_lookback) >= 2:
            price_trend = closes[-1] - closes[-15]
            macd_trend = m_lookback[-1] - m_lookback[-15]
            if price_trend < 0 and macd_trend > 0:
                macd_divergence_bullish = True
            elif price_trend > 0 and macd_trend < 0:
                macd_divergence_bearish = True

        # ৩. Equal Low / High (Swing Prominence=5, Buffer=0.0025)
        buffer = 0.0025
        is_equal_low = False
        is_equal_high = False
        
        curr_low = lows[-1]
        curr_high = highs[-1]
        
        for j in range(-25, -5):
            # Equal Low Check
            if abs(lows[j] - curr_low) <= buffer:
                if lows[j] == min(lows[j-2:j+3]):
                    is_equal_low = True
            # Equal High Check
            if abs(highs[j] - curr_high) <= buffer:
                if highs[j] == max(highs[j-2:j+3]):
                    is_equal_high = True

        # ৪. সিগন্যাল কন্ডিশন ম্যাচিং
        # Buy Signal
        if current_close < current_ema200 and is_equal_low and macd_divergence_bullish:
            return {"type": "BUY", "price": current_close}
            
        # Sell Signal
        if current_close > current_ema200 and is_equal_high and macd_divergence_bearish:
            return {"type": "SELL", "price": current_close}
            
        return None
    except Exception:
        return None

# --- UI Layout স্বাধীন ২ কলাম ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Live Buy Signals")
    # কন্টেইনার লিস্ট জেনারেট করে রাখা যেন একটার পর একটা সাথে সাথে আউটপুট পুশ করা যায়
    buy_output_area = st.container()

with col2:
    st.subheader("🔴 Live Sell Signals")
    sell_output_area = st.container()

# লাইভ অ্যানিমেশন বক্সের জন্য খালি স্লট
live_status_box = st.empty()

# রিয়েলটাইম একটার পর একটা আউটপুট দেখানোর জন্য গ্লোবাল লিস্ট সেশন স্টেট ট্র্যাকিং
if "buy_signals_list" not in st.session_state:
    st.session_state.buy_signals_list = []
if "sell_signals_list" not in st.session_state:
    st.session_state.sell_signals_list = []

# পূর্বে সংরক্ষিত ডাটা স্ক্রিনে রিপ্রেজেন্ট করা (যদি থাকে)
with buy_output_area:
    for sig in st.session_state.buy_signals_list:
        st.markdown(sig, unsafe_allow_html=True)
with sell_output_area:
    for sig in st.session_state.sell_signals_list:
        st.markdown(sig, unsafe_allow_html=True)

total_coins = len(binance_symbols)

# লুপ স্টার্ট
for i, symbol in enumerate(binance_symbols):
    progress_perc = int(((i + 1) / total_coins) * 100)
    
    # ডাইনামিক লাইভ পপ-আপ অ্যানিমেশন বক্স
    live_status_box.markdown(f"""
        <div class="scanning-box">
            <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                🔍 বর্তমান স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({i+1}/{total_coins})
            </p>
            <div class="scanning-coin">{symbol}</div>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                বাইনান্স স্পট সার্ভার স্ক্যানিং চলমান...
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ইন্ডিকেটর অ্যানালাইসিস রান
    result = fetch_and_analyze_binance(symbol)
    
    if result:
        if result["type"] == "BUY":
            html_content = f"""
                <div class="signal-card buy-card">
                    <h3>🟢 {symbol} - BUY SIGNAL</h3>
                    <p>Price: ${result['price']}</p>
                    <small>Timeframe: H1 | Live Match</small>
                </div>
            """
            st.session_state.buy_signals_list.append(html_content)
            # সাথে সাথে আলাদা করে আউটপুট প্রদান (এক সাথে সব আসার অপেক্ষা করবে না)
            with buy_output_area:
                st.markdown(html_content, unsafe_allow_html=True)
                
            send_telegram_message(f"🟢 *BINANCE BUY SIGNAL DETECTED*\n\nSymbol: {symbol}\nPrice: ${result['price']}\nTF: 1 Hour\nMatrix: 200 EMA Down + Equal Low + MACD Divergence")
            
        elif result["type"] == "SELL":
            html_content = f"""
                <div class="signal-card sell-card">
                    <h3>🔴 {symbol} - SELL SIGNAL</h3>
                    <p>Price: ${result['price']}</p>
                    <small>Timeframe: H1 | Live Match</small>
                </div>
            """
            st.session_state.sell_signals_list.append(html_content)
            # সাথে সাথে আলাদা করে আউটপুট প্রদান
            with sell_output_area:
                st.markdown(html_content, unsafe_allow_html=True)
                
            send_telegram_message(f"🔴 *BINANCE SELL SIGNAL DETECTED*\n\nSymbol: {symbol}\nPrice: ${result['price']}\nTF: 1 Hour\nMatrix: 200 EMA Up + Equal High + MACD Divergence")

    # বিন্যান্স পাবলিক রেট লিমিট হ্যান্ডেল করার জন্য প্রতি রিকোয়েস্টে অল্প বিরতি (১০০% ক্র্যাশ ফ্রি ডিপ্লয়মেন্ট নিশ্চিত করতে)
    time.sleep(0.1)

# স্ক্যান সমাপ্তি বার্তা
live_status_box.success("✅ এই রাউন্ডের অটো-স্ক্যানিং সফলভাবে শেষ হয়েছে! ১ ঘণ্টা পর আবার স্ক্রিন রিলোড নিয়ে নতুন স্ক্যান শুরু হবে।")
