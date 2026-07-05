import asyncio
import random

RETRYABLE_STATUS = (429, 500, 502, 503, 504)

async def invoke_with_retry(chain, payload: dict, rate_limiter, run_config, max_attempts: int = 5 ) -> str:
    for attempt in range(1, max_attempts + 1):
        rate_limiter.acquire()
        try:
            result = await chain.ainvoke(payload, config=run_config)
            return result
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            if status_code not in RETRYABLE_STATUS:
                raise e
            if attempt == max_attempts:
                raise e
            delay = min((2 ** (attempt - 1)), 60.0)
            jitter = random.uniform(0.0, 0.3)
            print(f"[!] Network issue (Status {status_code}). " f"Retrying in {delay + jitter:.2f}s...")
            await asyncio.sleep(delay + jitter)