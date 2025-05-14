import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# 👤 Made by Soham Vyas
# -----------------------------------

# Page Configuration
st.set_page_config(page_title="Soham's Crypto Tracker", layout="wide")
st.title("📈 Soham's Crypto Price Tracker")
st.caption("Built with ❤️ by Soham Vyas | Real-time data powered by CoinGecko API")

# --- Coin & Currency Lists ---
coin_list = [
    "bitcoin", "ethereum", "dogecoin", "solana", "ripple", "cardano",
    "polkadot", "tron", "litecoin", "shiba-inu", "avalanche-2",
    "uniswap", "chainlink", "stellar", "aptos", "filecoin",
    "internet-computer", "vechain", "near", "arbitrum", "monero",
    "algorand", "tezos", "hedera", "the-graph"
]
vs_currency_list = ["usd", "inr", "eur"]

# --- Sidebar Options ---
st.sidebar.header("🔍 Options")
coin = st.sidebar.selectbox("📌 Select a Cryptocurrency", coin_list, index=0)
vs_currency = st.sidebar.selectbox("💱 Compare With Currency", vs_currency_list)

# Time range selection
st.sidebar.subheader("📆 Price Chart Range")
days = st.sidebar.selectbox(
    "Select time range:",
    options=["1", "7", "30", "90", "180", "365", "max"],
    format_func=lambda x: {
        "1": "1 Day", "7": "7 Days", "30": "1 Month", "90": "3 Months",
        "180": "6 Months", "365": "1 Year", "max": "All Time"
    }[x]
)

# --- API Fetching Functions ---
@st.cache_data(ttl=300)
def get_coin_data(coin, vs):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    return requests.get(url, params={"localization": "false"}).json()

@st.cache_data(ttl=300)
def get_chart_data(coin, vs, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": vs, "days": days}
    res = requests.get(url, params=params).json()
    df = pd.DataFrame(res["prices"], columns=["Time", "Price"])
    df["Time"] = pd.to_datetime(df["Time"], unit="ms")
    return df

# --- Main Data Display ---
try:
    data = get_coin_data(coin, vs_currency)
    coin_name = data["name"]
    price = data["market_data"]["current_price"][vs_currency]
    change = data["market_data"]["price_change_percentage_24h"]
    cap = data["market_data"]["market_cap"][vs_currency]
    logo = data["image"]["large"]

    # Display current data
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(logo, width=64)
    with col2:
        st.subheader(f"{coin_name} ({coin.upper()})")
        st.metric("💰 Current Price", f"{price:.2f} {vs_currency.upper()}", f"{change:.2f}%")
        st.caption(f"Market Cap: {cap:,} {vs_currency.upper()}")
    with col3:
        st.markdown("")

    # Display price chart
    chart_df = get_chart_data(coin, vs_currency, days)
    titles = {
        "1": "1 Day", "7": "7 Days", "30": "1 Month", "90": "3 Months",
        "180": "6 Months", "365": "1 Year", "max": "All Time"
    }
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_df["Time"],
        y=chart_df["Price"],
        mode="lines",
        name=coin,
        line=dict(color="orange")
    ))
    fig.update_layout(
        title=f"{coin_name} - {titles[days]} Price Chart",
        xaxis_title="Date",
        yaxis_title=f"Price ({vs_currency.upper()})",
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("⚠️ Failed to load data. Please check your internet connection or CoinGecko API rate limits.")

# --- Footer ---
st.markdown("---")
st.markdown("[🌐 GitHub Repo](https://github.com/vyassoham/crypto-tracker) | [🚀 Deployed App](https://your-app-link.streamlit.app)")
