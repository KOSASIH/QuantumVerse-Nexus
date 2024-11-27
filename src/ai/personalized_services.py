import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class UserProfile:
    """Class to manage user profiles and preferences."""
    
    def __init__(self, user_id, preferences):
        """
        Initialize the UserProfile class.
        
        :param user_id: Unique identifier for the user.
        :param preferences: Dictionary of user preferences.
        """
        self.user_id = user_id
        self.preferences = preferences

class PersonalizedServices:
    """A system for providing personalized services based on user profiles."""
    
    def __init__(self):
        """Initialize the PersonalizedServices class."""
        self.user_profiles = {}
        self.service_data = pd.DataFrame()  # DataFrame to hold service information

    def add_user_profile(self, user_id, preferences):
        """Add a new user profile."""
        self.user_profiles[user_id] = UserProfile(user_id, preferences)
        logging.info(f"Added user profile for user_id: {user_id}")

    def load_service_data(self, data):
        """Load service data into the system."""
        self.service_data = pd.DataFrame(data)
        logging.info("Service data loaded.")

    def recommend_services(self, user_id):
        """Recommend services based on user preferences."""
        if user_id not in self.user_profiles:
            logging.error("User  profile not found.")
            return None
        
        user_preferences = self.user_profiles[user_id].preferences
        logging.info(f"Generating recommendations for user_id: {user_id}")

        # Calculate similarity scores
        service_features = self.service_data.drop(columns=['service_id'])
        user_vector = np.array([user_preferences.get(col, 0) for col in service_features.columns]).reshape(1, -1)

        # Standardize features
        scaler = StandardScaler()
        service_features_scaled = scaler.fit_transform(service_features)
        user_vector_scaled = scaler.transform(user_vector)

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(user_vector_scaled, service_features_scaled)
        self.service_data['similarity'] = similarity_scores.flatten()

        # Recommend top 5 services
        recommendations = self.service_data.sort_values(by='similarity', ascending=False).head(5)
        return recommendations[['service_id', 'service_name', 'similarity']]

# Example usage
if __name__ == "__main__":
    # Sample service data
    service_data = [
        {'service_id': 1, 'service_name': 'Personalized Fitness Plan', 'fitness': 5, 'nutrition': 3, 'wellness': 2},
        {'service_id': 2, 'service_name': 'Yoga Classes', 'fitness': 4, 'nutrition': 2, 'wellness': 5},
        {'service_id': 3, 'service_name': 'Meal Prep Service', 'fitness': 1, 'nutrition': 5, 'wellness': 3},
        {'service_id': 4, 'service_name': 'Meditation App', 'fitness': 2, 'nutrition': 1, 'wellness': 5},
        {'service_id': 5, 'service_name': 'Nutrition Coaching', 'fitness': 3, 'nutrition': 5, 'wellness': 2},
    ]

    # Initialize the personalized services system
    personalized_services = PersonalizedServices()
    personalized_services.load_service_data(service_data)

    # Add user profiles
    personalized_services.add_user_profile('user_1', {'fitness': 5, 'nutrition': 2, 'wellness': 3})
    personalized_services.add_user_profile('user_2', {'fitness': 2, 'nutrition': 5, 'wellness': 4})

    # Generate recommendations
    recommendations_user_1 = personalized_services.recommend_services('user_1')
    print("Recommendations for user_1:")
    print(recommendations_user_1)

    recommendations_user_2 = personalized_services.recommend_services('user_2')
    print("Recommendations for user_2:")
    print(recommendations_user_2)
