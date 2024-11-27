import re
from typing import Any, Dict, List

def is_valid_email(email: str) -> bool:
    """Validate an email address using a regular expression."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_url(url: str) -> bool:
    """Validate a URL using a regular expression."""
    url_regex = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+)(\.[a-zA-Z]{2,})(/.*)?$'
    return re.match(url_regex, url) is not None

def flatten_dict(nested_dict: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary."""
    items = {}
    for k, v in nested_dict.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries."""
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            dict1[key] = deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1

def generate_random_string(length: int) -> str:
    """Generate a random string of fixed length."""
    import random
    import string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def paginate_list(data: List[Any], page: int, page_size: int) -> List[Any]:
    """Paginate a list of data."""
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]

# Example usage
if __name__ == "__main__":
    # Test the helper functions
    print(is_valid_email("test@example.com"))  # True
    print(is_valid_url("https://www.example.com"))  # True
    print(flatten_dict({'a': 1, 'b': {'c': 2, 'd': 3}}))  # {'a': 1, 'b.c': 2, 'b.d': 3}
    print(deep_merge({'a': 1, 'b': {'c': 2}}, {'b': {'d': 3}, 'e': 4}))  # {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    print(generate_random_string(10))  # Random string of length 10
    print(paginate_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], page=2, page_size=3))  # [4, 5, 6]
