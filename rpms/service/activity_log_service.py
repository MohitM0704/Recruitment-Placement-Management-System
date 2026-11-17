"""
Activity Log Service for logging system events to file.
"""
from datetime import datetime
import os


class ActivityLogService:
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "activity_log.txt")

    def log(self, message: str) -> None:
        """Append a timestamped log message to the log file."""
        try:
            with open(self.LOG_FILE, "a", encoding="utf-8") as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {message}\n")
        except Exception as e:
            print(f"[Log Error]: {e}")
