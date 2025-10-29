
import time
from fastapi import Request
from starlette.responses import Response
from collections import defaultdict

BUCKET = defaultdict(lambda: {'tokens': 20, 'last': time.time()})
RATE = 10
INTERVAL = 60

async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host if request.client else 'unknown'
    b = BUCKET[ip]
    now = time.time()
    elapsed = now - b['last']
    b['tokens'] = min(20, b['tokens'] + elapsed * (RATE/INTERVAL))
    b['last'] = now
    if b['tokens'] < 1:
        return Response('Too many requests', status_code=429)
    b['tokens'] -= 1
    response = await call_next(request)
    return response
