# trading_bot_example.py
from src.trading.trading_bot import TradingBot

def run_trading_bot():
    """Example of using the AI-powered trading bot."""
    
    # Create a trading bot instance
    trading_bot = TradingBot(api_key='your_api_key', api_secret='your_api_secret')

    # Example trading strategy (replace with actual strategy)
    trading_strategy = {
        'buy_threshold': 0.05,  # Buy if price increases by 5%
        'sell_threshold': -0.05,  # Sell if price decreases by 5%
        'investment_amount': 100  # Amount to invest
    }

    # Start the trading bot
    trading_bot.start(trading_strategy)
    print("Trading bot is now running with the specified strategy.")

if __name__ == "__main__":
    run_trading_bot()
