"""
📈 Stock Price Tracker
Uses the yfinance library (free, no API key needed).

Install dependencies:
    pip install yfinance

Run:
    python stock_tracker.py
"""

import yfinance as yf
from datetime import datetime


def get_stock_info(ticker: str) -> None:
    """Fetch and display key info for a given stock ticker."""
    print(f"\n🔍 Looking up: {ticker.upper()}...")
    stock = yf.Ticker(ticker)
    info = stock.info

    # Some tickers return minimal info if invalid
    name = info.get("longName") or info.get("shortName")
    if not name:
        print("❌ Ticker not found. Please check the symbol and try again.")
        return

    # Pull key fields (use .get() so missing fields don't crash the app)
    price        = info.get("currentPrice") or info.get("regularMarketPrice")
    prev_close   = info.get("previousClose")
    day_high     = info.get("dayHigh")
    day_low      = info.get("dayLow")
    volume       = info.get("volume")
    market_cap   = info.get("marketCap")
    sector       = info.get("sector", "N/A")
    week_52_high = info.get("fiftyTwoWeekHigh")
    week_52_low  = info.get("fiftyTwoWeekLow")

    # Calculate price change from previous close
    if price and prev_close:
        change    = price - prev_close
        change_pct = (change / prev_close) * 100
        arrow     = "▲" if change >= 0 else "▼"
        change_str = f"{arrow} ${change:+.2f} ({change_pct:+.2f}%)"
    else:
        change_str = "N/A"

    # Format market cap (e.g. 2,450,000,000 → $2.45B)
    def fmt_market_cap(mc):
        if mc is None:
            return "N/A"
        if mc >= 1_000_000_000_000:
            return f"${mc / 1_000_000_000_000:.2f}T"
        if mc >= 1_000_000_000:
            return f"${mc / 1_000_000_000:.2f}B"
        if mc >= 1_000_000:
            return f"${mc / 1_000_000:.2f}M"
        return f"${mc:,.0f}"

    print("\n" + "=" * 45)
    print(f"  {name} ({ticker.upper()})")
    print("=" * 45)
    print(f"  💵 Current Price : ${price:.2f}" if price else "  💵 Current Price : N/A")
    print(f"  📊 Change        : {change_str}")
    print(f"  🔺 Day High      : ${day_high:.2f}" if day_high else "  🔺 Day High      : N/A")
    print(f"  🔻 Day Low       : ${day_low:.2f}" if day_low else "  🔻 Day Low       : N/A")
    print(f"  📦 Volume        : {volume:,}" if volume else "  📦 Volume        : N/A")
    print(f"  🏦 Market Cap    : {fmt_market_cap(market_cap)}")
    print(f"  🏭 Sector        : {sector}")
    print(f"  📅 52-Wk High    : ${week_52_high:.2f}" if week_52_high else "  📅 52-Wk High    : N/A")
    print(f"  📅 52-Wk Low     : ${week_52_low:.2f}" if week_52_low else "  📅 52-Wk Low     : N/A")
    print("=" * 45)


def get_price_history(ticker: str, period: str = "1mo") -> None:
    """Print recent closing prices for a stock."""
    stock = yf.Ticker(ticker)

    # Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    history = stock.history(period=period)

    if history.empty:
        print("❌ No historical data found.")
        return

    print(f"\n📅 Recent Closing Prices for {ticker.upper()} (last {period}):")
    print("-" * 30)
    for date, row in history.iterrows():
        date_str = date.strftime("%Y-%m-%d")
        print(f"  {date_str}  |  ${row['Close']:.2f}")
    print("-" * 30)


def main():
    print("=" * 45)
    print("       📈 Stock Price Tracker")
    print(f"       {datetime.now().strftime('%B %d, %Y  %I:%M %p')}")
    print("=" * 45)
    print("Examples: AAPL, TSLA, GOOGL, AMZN, MSFT")

    while True:
        print("\nOptions:")
        print("  1 - Look up a stock")
        print("  2 - View price history")
        print("  3 - Track multiple stocks")
        print("  q - Quit")

        choice = input("\nEnter choice: ").strip().lower()

        if choice == "q":
            print("\n👋 Goodbye!\n")
            break

        elif choice == "1":
            ticker = input("Enter stock ticker: ").strip()
            if ticker:
                get_stock_info(ticker)

        elif choice == "2":
            ticker = input("Enter stock ticker: ").strip()
            print("Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y")
            period = input("Enter period (default 1mo): ").strip() or "1mo"
            if ticker:
                get_price_history(ticker, period)

        elif choice == "3":
            tickers_input = input("Enter tickers separated by commas (e.g. AAPL, TSLA, AMZN): ")
            tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]
            for t in tickers:
                get_stock_info(t)

        else:
            print("⚠️  Invalid option. Please enter 1, 2, 3, or q.")


if __name__ == "__main__":
    main()
