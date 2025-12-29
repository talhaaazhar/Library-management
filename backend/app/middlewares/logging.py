import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = None
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.exception(
                f"Unhandled error | {request.method} {request.url.path}"
            )
            raise
        finally:
            process_time = round(time.time() - start_time, 3)
            status_code = response.status_code if response else "ERROR"

            logger.info(
                f"{request.method} {request.url.path} "
                f"Status: {status_code} "
                f"Time: {process_time}s"
            )
