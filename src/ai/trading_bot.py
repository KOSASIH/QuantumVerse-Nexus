import pandas as pd
import numpy as np
import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class TradingBot:
    """A simple trading bot for executing trades based on strategies."""

    def __init__(self, api_key, base_url):
        """
        Initialize the TradingBot class with API credentials.
        
        :param api_key: API key for the trading platform.
        :param base_url: Base URL for the trading platform API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.balance = 10000  # Starting balance in USD
        self.position = 0  # Current position in the asset
        self.asset = 'BTC'  # Trading asset

    def fetch_market_data(self):
        """Fetch market data for the trading asset."""
        logging.info("Fetching market data...")
        response = requests.get(f"{self.base_url}/market_data/{self.asset}")
        if response.status_code == 200:
            data = response.json()
            return data['price']
        else:
            logging.error("Failed to fetch market data.")
            return None

    def simple_moving_average(self, prices, window=5):
        """Calculate the simple moving average."""
        return prices.rolling(window=window).mean()

    def trading_strategy(self, prices):
        """Implement a simple trading strategy based on moving averages."""
        logging.info("Executing trading strategy...")
        prices['SMA_5'] = self.simple_moving_average(prices['close'], window=5)
        prices['SMA_20'] = self.simple_moving_average(prices['close'], window=20)

        # Buy signal
        if prices['SMA_5'].iloc[-1] > prices['SMA_20'].iloc[-1] and self.position == 0:
            logging.info("Buy signal detected.")
            self.execute_trade('buy', prices['close'].iloc[-1])
        
        # Sell signal
        elif prices['SMA_5'].iloc[-1] < prices['SMA_20'].iloc[-1] and self.position > 0:
            logging.info("Sell signal detected.")
            self.execute_trade('sell', prices['close'].iloc[-1])

    def execute_trade(self, action, price):
        """Execute a trade action (buy/sell)."""
        if action == 'buy':
            amount_to_buy = self.balance / price
            self.position += amount_to_buy
            self.balance = 0
            logging.info(f"Executed buy: {amount_to_buy} {self.asset} at ${price:.2f}")
        
        elif action == 'sell':
            self.balance += self.position * price
            logging.info(f"Executed sell: {self.position} {self.asset} at ${price:.2f}")
            self.position = 0

    def run(self):
        """Run the trading bot."""
        while True:
            price = self.fetch_market_data()
            if price is not None:
                # Simulate fetching historical prices for strategy
                historical_prices = pd.DataFrame({
                    'close': np.random.uniform(low=30000, high=60000, size=100)  # Simulated historical prices
                })
                self.trading_strategy(historical_prices)
            time.sleep(60)  # Wait for 1 minute before the next iteration

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    base_url = "https://api.yourtradingplatform.com"

    trading_bot = TradingBot(api_key, base_url)
    trading_bot.run()
