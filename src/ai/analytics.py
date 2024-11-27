import pandas as pd
import numpy as np

class Analytics:
    """A class for performing analytics on dApp data."""

    def __init__(self, data):
        """
        Initialize the Analytics class with data.
        
        :param data: A DataFrame containing the data to analyze.
        """
        self.data = data

    def user_engagement(self):
        """Calculate user engagement metrics."""
        total_users = self.data['user_id'].nunique()
        total_posts = self.data['post_id'].count()
        engagement_rate = total_posts / total_users if total_users > 0 else 0
        
        print(f"Total Users: {total_users}")
        print(f"Total Posts: {total_posts}")
        print(f"Engagement Rate (Posts per User): {engagement_rate:.2f}")

    def transaction_volume(self):
        """Calculate transaction volume metrics."""
        total_transactions = self.data['transaction_id'].count()
        total_value = self.data['transaction_value'].sum()
        
        print(f"Total Transactions: {total_transactions}")
        print(f"Total Transaction Value: {total_value:.2f} ETH")

    def nft_sales_analysis(self):
        """Analyze NFT sales data."""
        nft_sales = self.data[self.data['transaction_type'] == 'sale']
        total_nft_sales = nft_sales['transaction_id'].count()
        total_nft_value = nft_sales['transaction_value'].sum()
        
        print(f"Total NFT Sales: {total_nft_sales}")
        print(f"Total NFT Sales Value: {total_nft_value:.2f} ETH")

    def average_stake_per_user(self):
        """Calculate the average stake per user."""
        staking_data = self.data[self.data['transaction_type'] == 'stake']
        total_staked = staking_data['transaction_value'].sum()
        total_users_staking = staking_data['user_id'].nunique()
        
        average_stake = total_staked / total_users_staking if total_users_staking > 0 else 0
        
        print(f"Total Staked: {total_staked:.2f} ETH")
        print(f"Average Stake per User: {average_stake:.2f} ETH")

    def generate_report(self):
        """Generate a comprehensive report of the analytics."""
        print("=== Analytics Report ===")
        self.user_engagement()
        self.transaction_volume()
        self.nft_sales_analysis()
        self.average_stake_per_user()
        print("========================")

# Example usage
if __name__ == "__main__":
    # Sample data creation for demonstration
    data = {
        'user_id': [1, 2, 1, 3, 2, 1, 4],
        'post_id': [101, 102, 103, 104, 105, 106, 107],
        'transaction_id': [201, 202, 203, 204, 205, 206, 207],
        'transaction_value': [0.5, 1.0, 0.75, 2.0, 0.25, 1.5, 0.1],
        'transaction_type': ['stake', 'sale', 'sale', 'stake', 'sale', 'stake', 'stake']
    }
    
    df = pd.DataFrame(data)
    
    analytics = Analytics(df)
    analytics.generate_report()
