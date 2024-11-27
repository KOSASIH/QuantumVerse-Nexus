# data_validation.py
import re

class DataValidation:
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate a blockchain address format."""
        # Example regex for a hypothetical blockchain address
        address_regex = r'^[a-zA-Z0-9]{34}$'
        return re.match(address_regex, address) is not None

    @staticmethod
    def validate_transaction_amount(amount: float) -> bool:
        """Validate the transaction amount."""
        return amount > 0

    @staticmethod
    def validate_signature(signature: str) -> bool:
        """Validate a digital signature format."""
        # Example regex for a hypothetical signature
        signature_regex = r'^[a-fA-F0-9]{128}$'
        return re.match(signature_regex, signature) is not None

    @staticmethod
    def validate_transaction_data(data: dict) -> bool:
        """Validate transaction data structure."""
        required_fields = ['from', 'to', 'amount', 'signature']
        return all(field in data for field in required_fields) and \
               DataValidation.validate_address(data['from']) and \
               DataValidation.validate_address(data['to']) and \
               DataValidation.validate_transaction_amount(data['amount']) and \
               DataValidation.validate_signature(data['signature'])
