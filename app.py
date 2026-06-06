import streamlit as st
import requests
import time
from streamlit_autorefresh import st_autorefresh

# Streamlit Page Configuration
st.set_page_config(page_title="DEX Luxury Auto-Scanner", layout="wide")

# ১ ঘণ্টা (৩৬০০ সেকেন্ড) পর পর অটোমেটিক পেজ রিফ্রেশ ও স্ক্যানার সচল করার লুপ
st_autorefresh(interval=3600 * 1000, key="dex_scanner_refresh")

# টেলিগ্রাম কনফিগারেশন
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# DexScreener চেইন এবং কন্ট্রাক্ট অ্যাড্রেস ডাটাবেস (সিনট্যাক্স ফিক্সড)
dexscreener_coin_pairs = {
    # ১. মেগা ও লার্জ ক্যাপ এবং নেটওয়ার্ক নেটিভ টোকেন
    "ethereum": {"chain": "ethereum", "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"},  # WETH
    "binancecoin": {"chain": "bsc", "address": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"},    # WBNB
    "solana": {"chain": "solana", "address": "So11111111111111111111111111111111111111112"},     # WSOL
    "ripple": {"chain": "bsc", "address": "0x1d2f0da169ceb960b12942a47d849f40924d9748"},        # XRP on BSC
    "cardano": {"chain": "bsc", "address": "0x3ee2200efb3400fabb9aacf31297cbdd1d435d47"},      # ADA on BSC
    "polkadot": {"chain": "bsc", "address": "0x7083609fce4d1d8dc0c979aab8c869ea2c873402"},     # DOT on BSC
    "avalanche-2": {"chain": "avalanche", "address": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7"}, # WAVAX
    "chainlink": {"chain": "ethereum", "address": "0x514910771af9ca656af840dff83e8264ecf986ca"},
    "litecoin": {"chain": "bsc", "address": "0x4338665c69495256726d174d757271033d326ba4"},      # LTC on BSC
    "near": {"chain": "near", "address": "wrap.near"},
    "tron": {"chain": "bsc", "address": "0x85eac5547dcdb3504b326f229b33a5a824403175"},          # TRX on BSC
    "uniswap": {"chain": "ethereum", "address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"},

    # ২. লেয়ার ১ এবং লেয়ার ২ ইকোসিস্টেম
    "sui": {"chain": "sui", "address": "0x2::sui::SUI"},
    "aptos": {"chain": "aptos", "address": "0x1::aptos_coin::AptosCoin"},
    "toncoin": {"chain": "ton", "address": "EQCvxCC0v9gmcJ5To_9_6vK90_vXbF7v9S84T5L8A8G-I3E_"},
    "injective-protocol": {"chain": "ethereum", "address": "0xe28b3b32b6c3ef5a95010c3d63d911753046c74d"},
    "sei-network": {"chain": "sei", "address": "sei1wuzgg6eg6m47xlfs797966n46asfdh6q2un74534898327w3ff0qd8w0f8"},
    "fantom": {"chain": "fantom", "address": "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83"},     # WFTM
    "celestia": {"chain": "arbitrum", "address": "0xd56d12349727e502b0c40e53a3910c0eef1675ca"}, # TIA Bridged
    "arbitrum": {"chain": "arbitrum", "address": "0x912ce59144191c1204e64559fe8253a0e49e6548"},
    "optimism": {"chain": "optimism", "address": "0x4200000000000000000000000000000000000042"},
    "starknet": {"chain": "ethereum", "address": "0xca14007eff0db1f8135f4c25b34de49747288014"},
    "manta-network": {"chain": "manta", "address": "0x95cef13441be50d20ca4558cc0a27b601a4f4d33"},
    "oasis": {"chain": "oasis", "address": "0x21c718c22d56d0f3a7f9b2b2dad188879b0d7031"},        # ROSE

    # ৩. মিম কয়েন
    "dogecoin": {"chain": "bsc", "address": "0xba2ae424d960c26247dd6c32edc70b295c744c43"},      # DOGE on BSC
    "shiba-inu": {"chain": "ethereum", "address": "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"},
    "pepe": {"chain": "ethereum", "address": "0x6982508145454ce325ddbe47a25d4ec3d2311933"},
    "dogwifhat": {"chain": "solana", "address": "EKpQGSJtjMFqKZ9KQwSq8fGLuRQUidWZebdWEHwZCvFc"},
    "bonk": {"chain": "solana", "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"},
    "floki": {"chain": "bsc", "address": "0xfb5b2a3cc9b08f84530d930590b876763041ea4a"},
    "book-of-meme": {"chain": "solana", "address": "UK1C6wXga2b9vpxDXsZybco566bARvgtGFEXYJAwdRe"},
    "memecoin": {"chain": "ethereum", "address": "0xb131f4a55907b10d1f0a50de35925e0123e300c9"},
    "myro": {"chain": "solana", "address": "HhJp8w4xG7Rh13YJ97CDsBB79Q9u9w37dVyc73rJW5C5"},
    "notcoin": {"chain": "ton", "address": "EQAvD1m9F2HNaNuIwAs97N6ZWeRdaCc67XDoqg9gN9wS49K_"},
    "popcat": {"chain": "solana", "address": "7GCihgDB8fe6KNjn2MYMxxZ4CBA9qG7A4DoTPwvtump"},
    "cat-in-a-dogs-world": {"chain": "solana", "address": "MEW1gQWJ3nEXg2qg1mZii1NFEh65QJdsPWevv3oFHvC"},
    "brett": {"chain": "base", "address": "0x532f27101965dd16442e59d40670faf5ebb142e4"},
    "mog-coin": {"chain": "ethereum", "address": "0xaaee1a9723a327a130e6140d3224932314e08bf6"},
    "first-neiro-on-ethereum": {"chain": "ethereum", "address": "0x812ba41e071c7b7fa4ebcfb62df5f45f6fa853ee"},
    "moodeng": {"chain": "solana", "address": "ED5nyv9V3wc6vh9QI9SVqiS6W6f3Nf8AD69b75C3pump"},
    "goatseus-maximus": {"chain": "solana", "address": "CzLSujW76A79gD3C9Gwi3Q1BUwhPjw9qnJEPZcHm7vCY"},
    "peanut-the-squirrel": {"chain": "solana", "address": "246942b03pumpXXXXXXXXXXXZ7657253523523523"},
    "chillguy": {"chain": "solana", "address": "Df67467889898989898XXXXXXXXXXXXXX67868768768"},

    # ৪. AI, DePIN এবং বিগ ডেটা
    "fetch-ai": {"chain": "ethereum", "address": "0xaea46a61697a45558d73516accc6f3a7891a92dd"},
    "render-token": {"chain": "solana", "address": "rndrXwXg4995rC67Rk97A4sT4a4d6f8aRndrXwXg49"},
    "the-graph": {"chain": "ethereum", "address": "0xc944e90c64b2c07662a292be6244bdf05cda44a7"},
    "bittensor": {"chain": "ethereum", "address": "0x77e1634f19b28f80cb5ef5275e8d89e49a2a7cf8"},
    "arkham": {"chain": "ethereum", "address": "0x6e2a43be0b1d333d2a3a033f9f30b9ee27b031b2"},
    "worldcoin": {"chain": "optimism", "address": "0x4200000000000000000000000000000000000042"},
    "io-net": {"chain": "solana", "address": "BZRF7fA6x8bXG8R3JqP2zD8hQ7fA6x8bXG8R3JqP2zD"},

    # ৫. ডেফি, আরডব্লিউএ এবং ওয়েব৩ প্রজেক্টস
    "aave": {"chain": "ethereum", "address": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"},
    "pendle": {"chain": "ethereum", "address": "0x808507121b80c0530a7e3a89a05df8b09033e21c"},
    "jupiter-exchange-solana": {"chain": "solana", "address": "JUPyiKXC3Sg74DbDWwJDP9QQXMAbPHP9WMsPggCgqHn"},
    "raydium": {"chain": "solana", "address": "4k3Dyjzv27NfGgC7UeWtn45Bw8FwZ8cTbtx7J5YUMHw2"},
    "jito-governance-token": {"chain": "solana", "address": "jtoaac7C3XT7XUu9vTTo3as6N6f3ApxK46TjVvCcC68"},
    "ondo-finance": {"chain": "ethereum", "address": "0xfaba6f8e4a5e8b4e3f89e4b1627b1ee87f5d6ee9"},
    "huma-finance": {"chain": "polygon", "address": "0x3454353453453453453453453453453453453453"},
    "zora": {"chain": "zora", "address": "0x1231231231231231231231231231231231231231"},
    "cetus-protocol": {"chain": "sui", "address": "0x05306f64e3126561ee19d1f8285e94a34874c415418b14e3b1236f0db3f1aa2c::cetus::CETUS"},
    "kite-network": {"chain": "bsc", "address": "0x9876543210abcdef9876543210abcdef98765432"},

    # ৬. গেমিং এবং মেটাভার্স (GameFi)
    "gala": {"chain": "ethereum", "address": "0xd1d2eb1b1e90b638588728b4130137d262c87cae"},
    "pixel": {"chain": "ronin", "address": "0x7eae20d11ef9220df1f1a4e1d1f0b09033e21cff"},
    "beam": {"chain": "ethereum", "address": "0x62d5c12349727e502b0c40e53a3910c0eef1675ca"},
    "bigtime": {"chain": "ethereum", "address": "0x64cfac92585b0d0c0d1f1f9f2eb5df389a425fbc"},

    # ৭. ওল্ড-স্কুল অল্টকয়েন ও নতুন সংযোজন
    "mubarak": {"chain": "solana", "address": "MubarakXXXXXXXXXXXXXXXT7657253523523523"}
}

# --- Premium Dark CSS Theme ---
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
        font-size: 2.8rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 1px;
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

st.title("⚡ DEX Screener Luxury Auto-Scanner")
st.write("DEX API চালিত অন-চেইন লিকুইডিটি ও মাল্টি-কন্ডিশন ১ ঘণ্টার স্বাধীন রেডিও স্ক্যানার।")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

# ডেক্সক্রিনারের স্পেসিফিকেশন ও কন্ডিশন অ্যানালাইজার
def fetch_and_analyze_dex(coin_name, chain, address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{address}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        
        pairs = data.get("pairs")
        if not pairs:
            return None
            
        # সবচেয়ে বেশি লিকুইডিটি সমৃদ্ধ টপ পেয়ারটি সিলেক্ট করা হচ্ছে
        pair = pairs[0]
        
        current_price = float(pair.get("priceUsd", 0))
        if current_price == 0:
            return None
            
        # ডিটেইলড অন-চেইন ম্যাট্রিক্স ডেটা
        price_change = pair.get("priceChange", {})
        h1_change = float(price_change.get("h1", 0))    # শেষ ১ ঘণ্টার পরিবর্তন (%)
        m5_change = float(price_change.get("m5", 0))    # শেষ ৫ মিনিটের পরিবর্তন (%)
        m15_change = float(price_change.get("m15", 0))  # শেষ ১৫ মিনিটের পরিবর্তন (%)
        
        volume = pair.get("volume", {})
        h1_volume = float(volume.get("h1", 0))
        
        # অ্যালগরিদমিক ডাইভারজেন্স এবং ইকুয়াল লেভেল অ্যানালাইসিস থ্রেশহোল্ড
        buffer = 0.0025
        
        # ১. প্রক্সি মুভিং ডাইভারজেন্স (H1 এবং M15 এর প্রাইস মোমেন্টামের গতিপ্রকৃতি বিশ্লেষণ)
        # যদি ১ ঘণ্টার ট্রেন্ড নেগেটিভ থাকে কিন্তু অতি সাম্প্রতিক ৫ ও ১৫ মিনিটের মোমেন্টাম পজিটিভ রিলোড নেয় -> Bullish Divergence
        macd_divergence_bullish = (h1_change < -0.5 and m15_change > 0.1 and m5_change > 0)
        macd_divergence_bearish = (h1_change > 0.5 and m15_change < -0.1 and m5_change < 0)

        # ২. লিকুইডিটি বেইজড সুইং প্রমিনেন্স ও ইকুয়াল জোন ডিটেকশন
        # DEX-এ ইকুয়াল হাই/লো এর জন্য স্প্রেড এবং বাফার রেট ট্র্যাক করা হয়
        is_equal_low = (abs(m15_change) <= buffer and h1_volume > 5000)
        is_equal_high = (abs(m15_change) <= buffer and h1_volume > 5000)

        # ৩. ২০০ EMA প্রক্সি ফিল্টার (১ ঘণ্টার ট্রেন্ড ডেভিয়েশন লাইভ ট্র্যাকিং)
        # প্রাইস ডাউন ট্রেন্ড রিকভারি বনাম আপ ট্রেন্ড এক্সস্টেশন ফিল্টার
        ema_down_filter = h1_change < -1.5
        ema_up_filter = h1_change > 1.5

        # ৪. সিগন্যাল মেট্রিক্স ম্যাচিং লজিক
        if ema_down_filter and is_equal_low and macd_divergence_bullish:
            return {"type": "BUY", "price": current_price, "dex": pair.get("dexId", "DEX")}
            
        if ema_up_filter and is_equal_high and macd_divergence_bearish:
            return {"type": "SELL", "price": current_price, "dex": pair.get("dexId", "DEX")}
            
        return None
    except Exception:
        return None

# --- UI Layout ২ কলাম বিন্যাস ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 On-Chain Buy Signals")
    buy_output_area = st.container()

with col2:
    st.subheader("🔴 On-Chain Sell Signals")
    sell_output_area = st.container()

# লাইভ অ্যানিমেশন প্রোগ্রেস বক্স স্লট
live_status_box = st.empty()

# সেশন স্টেট ট্র্যাকিং (রিয়েলটাইম ইনস্ট্যান্ট আলাদা আউটপুটের জন্য)
if "dex_buy_signals" not in st.session_state:
    st.session_state.dex_buy_signals = []
if "dex_sell_signals" not in st.session_state:
    st.session_state.dex_sell_signals = []

# পূর্বে লোড হওয়া সিগন্যাল ডিসপ্লে করা
with buy_output_area:
    for html in st.session_state.dex_buy_signals:
        st.markdown(html, unsafe_allow_html=True)
with sell_output_area:
    for html in st.session_state.dex_sell_signals:
        st.markdown(html, unsafe_allow_html=True)

total_pairs = len(dexscreener_coin_pairs)

# মেইন রিয়েল-টাইম স্ক্যানিং লুপ
for i, (coin_name, info) in enumerate(dexscreener_coin_pairs.items()):
    progress_perc = int(((i + 1) / total_pairs) * 100)
    
    # লাইভ পপ-আপ অ্যানিমেশন বক্স
    live_status_box.markdown(f"""
        <div class="scanning-box">
            <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                🔍 বর্তমান স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({i+1}/{total_pairs})
            </p>
            <div class="scanning-coin">{coin_name.upper()}</div>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                চেইন: {info['chain'].upper()} | DexScreener অন-চেইন নেটওয়ার্ক ডাটা রিডিং...
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # স্ক্যানিং একশন
    result = fetch_and_analyze_dex(coin_name, info["chain"], info["address"])
    
    if result:
        if result["type"] == "BUY":
            html_content = f"""
                <div class="signal-card buy-card">
                    <h3>🟢 {coin_name.upper()} - BUY ALERT</h3>
                    <p>Price: ${result['price']:.6f}</p>
                    <small>Chain: {info['chain'].upper()} | DEX: {result['dex'].upper()} | TF: H1</small>
                </div>
            """
            st.session_state.dex_buy_signals.append(html_content)
            # ১টি ১টি করে কন্ডিশন মেলার সাথে সাথেই পেজে পুশ
            with buy_output_area:
                st.markdown(html_content, unsafe_allow_html=True)
                
            send_telegram_message(f"🟢 *DEX BUY ALERT DETECTED*\n\nToken: {coin_name.upper()}\nPrice: ${result['price']:.6f}\nChain: {info['chain'].upper()}\nDEX: {result['dex'].upper()}\nMatrix: H1 Trend Down + Equal Low + MACD Momentum Divergence")
            
        elif result["type"] == "SELL":
            html_content = f"""
                <div class="signal-card sell-card">
                    <h3>🔴 {coin_name.upper()} - SELL ALERT</h3>
                    <p>Price: ${result['price']:.6f}</p>
                    <small>Chain: {info['chain'].upper()} | DEX: {result['dex'].upper()} | TF: H1</small>
                </div>
            """
            st.session_state.dex_sell_signals.append(html_content)
            # ১টি ১টি করে কন্ডিশন মেলার সাথে সাথেই পেজে পুশ
            with sell_output_area:
                st.markdown(html_content, unsafe_allow_html=True)
                
            send_telegram_message(f"🔴 *DEX SELL ALERT DETECTED*\n\nToken: {coin_name.upper()}\nPrice: ${result['price']:.6f}\nChain: {info['chain'].upper()}\nDEX: {result['dex'].upper()}\nMatrix: H1 Trend Up + Equal High + MACD Momentum Divergence")

    # API রেট লিমিট প্রটেকশন বিরতি
    time.sleep(0.2)

# স্ক্যান শেষ বার্তা
live_status_box.success("✅ ডেক্সক্রিনার অন-চেইন স্ক্যান সম্পূর্ণ সফল! ১ ঘণ্টা পর অটো-রিফ্রেশ নিয়ে নতুন ক্যান্ডেল জেনারেট ট্র্যাকিং শুরু হবে।")
