import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging.correlation import set_correlation_id
from app.core.logging.logger import get_logger

logger = get_logger("http")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # ✅ Libera OPTIONS
        if request.method == "OPTIONS":
            return await call_next(request)

        correlation_id = request.headers.get("X-Correlation-ID")
        set_correlation_id(correlation_id)

        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                f"Unhandled error {request.method} {request.url.path}"
            )
            raise

        response.headers["X-Correlation-ID"] = correlation_id or ""
        response.headers["X-Process-Time"] = str(
            round(time.time() - start_time, 4)
        )
        return response

