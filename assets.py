# ============================================================================
# JEXA Assets Database
# ============================================================================

# Stocks
STOCKS = {
    # Tech Giants
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", "AMZN": "Amazon",
    "META": "Meta", "TSLA": "Tesla", "NVDA": "NVIDIA", "AMD": "AMD",
    
    # AI & Semiconductors  
    "AVGO": "Broadcom", "QCOM": "Qualcomm", "INTC": "Intel", "MU": "Micron",
    "ASML": "ASML", "TSM": "Taiwan Semi", "ARM": "ARM", "SMCI": "Super Micro",
    "AMAT": "Applied Materials", "LRCX": "Lam Research", "KLAC": "KLA",
    
    # Cloud & Software
    "CRM": "Salesforce", "ORCL": "Oracle", "ADBE": "Adobe", "NOW": "ServiceNow",
    "SNOW": "Snowflake", "DDOG": "Datadog", "NET": "Cloudflare", "CRWD": "CrowdStrike",
    "PANW": "Palo Alto", "PLTR": "Palantir", "MDB": "MongoDB",
    
    # EV & Auto
    "RIVN": "Rivian", "LCID": "Lucid", "F": "Ford", "GM": "GM",
    "NIO": "NIO", "XPEV": "XPeng", "LI": "Li Auto",
    
    # Fintech
    "SQ": "Block", "PYPL": "PayPal", "COIN": "Coinbase", "HOOD": "Robinhood",
    "SOFI": "SoFi", "V": "Visa", "MA": "Mastercard",
    
    # E-commerce
    "SHOP": "Shopify", "BABA": "Alibaba", "MELI": "MercadoLibre", "ETSY": "Etsy",
    
    # Entertainment
    "NFLX": "Netflix", "DIS": "Disney", "SPOT": "Spotify", "RBLX": "Roblox",
    
    # Others
    "JPM": "JPMorgan", "BAC": "Bank of America", "WFC": "Wells Fargo",
}

# Crypto
CRYPTO = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum", 
    "BNB-USD": "Binance Coin",
    "SOL-USD": "Solana",
    "XRP-USD": "Ripple",
    "ADA-USD": "Cardano",
    "DOGE-USD": "Dogecoin",
    "AVAX-USD": "Avalanche",
    "MATIC-USD": "Polygon",
    "DOT-USD": "Polkadot",
}

# Combine all
ALL_ASSETS = {**STOCKS, **CRYPTO}

# Categories
CATEGORIES = {
    "Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
    "AI & Semiconductors": ["NVDA", "AMD", "SMCI", "ARM", "AVGO", "PLTR", "ASML"],
    "Electric Vehicles": ["TSLA", "RIVN", "LCID", "NIO", "XPEV"],
    "Fintech": ["SQ", "PYPL", "COIN", "HOOD", "SOFI", "V", "MA"],
    "E-commerce": ["SHOP", "AMZN", "BABA", "MELI", "ETSY"],
    "Streaming": ["NFLX", "DIS", "SPOT", "RBLX"],
    "Top Crypto": ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"],
}

# Watchlists
WATCHLISTS = {
    "🔥 Hot Stocks": ["NVDA", "TSLA", "PLTR", "SMCI", "AMD", "COIN"],
    "💎 Value Picks": ["AAPL", "MSFT", "GOOGL", "META", "AMZN"],
    "🚀 Growth": ["RIVN", "LCID", "SNOW", "DDOG", "CRWD"],
    "💰 Crypto": ["BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD"],
}