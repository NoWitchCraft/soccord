import time
from collections import defaultdict

class SlidingWindowTracker:
    def __init__(self, threshold_count: int = 5, window_seconds: int = 60):
        self.threshold_count = threshold_count
        self.window_seconds = window_seconds
        self.attempts = defaultdict(list)
        self.alerted_keys = set()

    def register_attempt(self, key: str) -> bool:
        """
        Registers an event for a specific key (e.g., IP address or username).
        Returns True if the threshold was crossed for the first time in the current window.
        """
        now = time.time()
        # Clean up timestamps outside the time window
        self.attempts[key] = [
            ts for ts in self.attempts[key] if now - ts <= self.window_seconds
        ]
        
        self.attempts[key].append(now)

        if len(self.attempts[key]) >= self.threshold_count:
            if key not in self.alerted_keys:
                self.alerted_keys.add(key)
                return True
        return False

    def reset(self, key: str):
        """Resets tracking state upon successful event (e.g., successful login)."""
        self.attempts.pop(key, None)
        self.alerted_keys.discard(key)