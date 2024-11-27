import os

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    API_KEY = os.getenv('API_KEY', 'your-default-api-key')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DATABASE_URI = os.getenv('PROD_DATABASE_URI', 'sqlite:///prod.db')
    LOG_LEVEL = 'ERROR'
