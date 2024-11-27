import unittest
import time
from performance import Performance

class TestPerformance(unittest.TestCase):
    def test_fibonacci_performance(self):
        """Test the performance of the Fibonacci function."""
        start_time = time.time()
        result = Performance.fibonacci(30)  # A reasonable number for testing
        end_time = time.time()
        
        self.assertEqual(result, 832040)  # Known result for Fibonacci(30)
        self.assertLess(end_time - start_time, 2)  # Ensure it runs in less than 2 seconds

    def test_process_large_dataset_performance(self):
        """Test the performance of processing a large dataset."""
        large_data = list(range(1000000))  # 1 million elements
        start_time = time.time()
        result = Performance.process_large_dataset(large_data)
        end_time = time.time()
        
        self.assertEqual(len(result), 1000000)  # Ensure the output length is correct
        self.assertLess(end_time - start_time, 1)  # Ensure it runs in less than 1 second

if __name__ == '__main__':
    unittest.main()
