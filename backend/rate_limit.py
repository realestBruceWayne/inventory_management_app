from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, status
from functools import wraps

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Rate limit configurations
DEFAULT_RATE_LIMIT = "100/minute"  # 100 requests per minute
STRICT_RATE_LIMIT = "20/minute"    # 20 requests per minute for sensitive operations
AUTH_RATE_LIMIT = "10/minute"     # 10 requests per minute for auth operations

def rate_limit_error_handler(request: Request, exc: RateLimitExceeded):
    """Custom error handler for rate limit exceeded"""
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": "Rate limit exceeded",
            "message": str(exc),
            "retry_after": exc.retry_after if hasattr(exc, 'retry_after') else 60
        }
    )
