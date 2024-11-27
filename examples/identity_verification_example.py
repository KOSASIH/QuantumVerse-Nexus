# identity_verification_example.py
from src.identity_verification.verification_service import VerificationService

def perform_identity_verification():
    """Example of the identity verification process."""
    
    # Create a verification service instance
    verification_service = VerificationService()

    # Example user data (replace with actual user data)
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '123-456-7890',
        'government_id': 'A123456789'
    }

    # Perform identity verification
    verification_result = verification_service.verify_identity(user_data)
    
    if verification_result['status']:
        print("Identity verification successful!")
    else:
        print("Identity verification failed:", verification_result['message'])

if __name__ == "__main__":
    perform_identity_verification()
