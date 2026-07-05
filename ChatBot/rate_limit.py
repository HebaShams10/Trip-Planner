import time
import threading
from collections import deque

class RateLimiter:
    def __init__(self, rpm: int = 30, window_s: float = 60.0):
        self.rpm = rpm
        self.window_s = window_s
        self._req_timestamps = deque()
        self._lock = threading.Lock()

    def _purge_expired(self, now: float) -> None:
        cutoff = now - self.window_s
        while (
            self._req_timestamps
            and self._req_timestamps[0] < cutoff
        ):
            self._req_timestamps.popleft()

    def acquire(self, timeout: float = 90.0) -> bool:
        deadline = time.monotonic() + timeout
        while True:
            with self._lock:
                now = time.monotonic()
                self._purge_expired(now)
                if len(self._req_timestamps) < self.rpm:
                    self._req_timestamps.append(now)
                    return True
            if time.monotonic() > deadline:
                raise TimeoutError("Rate limit acquire timed out")
            time.sleep(0.5)

def test_rate_limit():
    limiter = RateLimiter(rpm=5, window_s=10)
    start = time.monotonic()
    for i in range(12):
        limiter.acquire()
        elapsed = time.monotonic() - start
        print(f"Request {i+1} allowed at {elapsed:.2f}s")
if __name__ == "__main__":
    test_rate_limit()