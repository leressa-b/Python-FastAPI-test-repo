from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class DummyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Intentional logic flaw: allows all requests
        response = await call_next(request)
        return response
