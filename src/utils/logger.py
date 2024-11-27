import logging
import os

class Logger:
    """Logger utility class for the application."""

    def __init__(self, name: str, log_file: str = None):
        """
        Initializes the logger.

        :param name: Name of the logger (usually the module name).
        :param log_file: Optional log file path. If None, logs will be printed to console.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set the default logging level

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Set level for console output

        # Create a formatter and set it for the console handler
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

        # If a log file is specified, create a file handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # Set level for file output
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)

# Example usage
if __name__ == "__main__":
    # Create a logger instance
    logger = Logger(name="MyAppLogger", log_file="app.log")

    # Log messages of various severity levels
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
