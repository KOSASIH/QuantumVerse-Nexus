# performance_monitor.py
import time
import psutil

class PerformanceMonitor:
    @staticmethod
    def get_cpu_usage() -> float:
        """Get the current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage() -> dict:
        """Get the current memory usage statistics."""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percentage': memory.percent
        }

    @staticmethod
    def log_performance_metrics():
        """Log performance metrics to console."""
        cpu_usage = PerformanceMonitor.get_cpu_usage()
        memory_usage = PerformanceMonitor.get_memory_usage()
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage['used'] / (1024 ** 2):.2f} MB used out of {memory_usage['total'] / (1024 ** 2):.2f} MB")
