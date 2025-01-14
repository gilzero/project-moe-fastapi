import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request
from starlette.responses import Response

class RequestIDMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        logging.info(f"Request {request_id} started.")
        response: Response = await call_next(request)
        logging.info(f"Request {request_id} completed.")
        response.headers["X-Request-ID"] = request_id
        return response
