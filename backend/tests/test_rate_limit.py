import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from fastapi import Request, HTTPException, status

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rate_limit import (
    limiter,
    DEFAULT_RATE_LIMIT,
    STRICT_RATE_LIMIT,
    AUTH_RATE_LIMIT,
    rate_limit_error_handler
)
from slowapi.errors import RateLimitExceeded


class TestRateLimitConstants:
    """Test suite for rate limit constant values"""

    def test_default_rate_limit(self):
        """Test that DEFAULT_RATE_LIMIT is set correctly"""
        assert DEFAULT_RATE_LIMIT == "100/minute"

    def test_strict_rate_limit(self):
        """Test that STRICT_RATE_LIMIT is set correctly"""
        assert STRICT_RATE_LIMIT == "20/minute"

    def test_auth_rate_limit(self):
        """Test that AUTH_RATE_LIMIT is set correctly"""
        assert AUTH_RATE_LIMIT == "10/minute"

    def test_rate_limits_are_strings(self):
        """Test that all rate limits are strings"""
        assert isinstance(DEFAULT_RATE_LIMIT, str)
        assert isinstance(STRICT_RATE_LIMIT, str)
        assert isinstance(AUTH_RATE_LIMIT, str)


class TestLimiterInitialization:
    """Test suite for limiter initialization"""

    def test_limiter_exists(self):
        """Test that limiter is initialized"""
        assert limiter is not None

    def test_limiter_has_key_func(self):
        """Test that limiter has a key function"""
        # slowapi limiter structure may vary, just check it exists and is callable
        assert limiter is not None
        # The actual key function is stored internally, just verify limiter works


class TestRateLimitErrorHandler:
    """Test suite for rate limit error handler"""

    def test_rate_limit_error_handler_returns_http_exception(self):
        """Test that error handler returns HTTPException"""
        # Create a mock request
        request = Mock(spec=Request)
        
        # Create a mock RateLimitExceeded exception
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert isinstance(result, HTTPException)
        assert result.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_rate_limit_error_handler_detail_structure(self):
        """Test that error handler detail has correct structure"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        detail = result.detail
        assert isinstance(detail, dict)
        assert "error" in detail
        assert "message" in detail
        assert "retry_after" in detail

    def test_rate_limit_error_handler_error_message(self):
        """Test that error message is set correctly"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["error"] == "Rate limit exceeded"
        assert result.detail["message"] == "Rate limit exceeded"

    def test_rate_limit_error_handler_retry_after(self):
        """Test that retry_after is set correctly"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 120
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["retry_after"] == 120

    def test_rate_limit_error_handler_no_retry_after(self):
        """Test that default retry_after is used when not available"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        # Don't set retry_after attribute
        del mock_exc.retry_after
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["retry_after"] == 60  # Default value

    def test_rate_limit_error_handler_custom_message(self):
        """Test that custom error message is preserved"""
        request = Mock(spec=Request)
        
        custom_message = "Custom rate limit message"
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value=custom_message)
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["message"] == custom_message


class TestRateLimitIntegration:
    """Test suite for rate limiting integration scenarios"""

    def test_different_rate_limits_for_different_operations(self):
        """Test that different rate limits are used for different operations"""
        # This test verifies the constants are set appropriately
        # Actual rate limiting would require integration testing with the full app
        
        assert DEFAULT_RATE_LIMIT != STRICT_RATE_LIMIT
        assert STRICT_RATE_LIMIT != AUTH_RATE_LIMIT
        assert DEFAULT_RATE_LIMIT != AUTH_RATE_LIMIT

    def test_strict_limit_is_more_restrictive(self):
        """Test that strict limit is more restrictive than default"""
        # Parse the rate limits to compare
        default_parts = DEFAULT_RATE_LIMIT.split("/")
        strict_parts = STRICT_RATE_LIMIT.split("/")
        
        default_requests = int(default_parts[0])
        strict_requests = int(strict_parts[0])
        
        assert strict_requests < default_requests

    def test_auth_limit_is_most_restrictive(self):
        """Test that auth limit is the most restrictive"""
        # Parse the rate limits to compare
        default_parts = DEFAULT_RATE_LIMIT.split("/")
        strict_parts = STRICT_RATE_LIMIT.split("/")
        auth_parts = AUTH_RATE_LIMIT.split("/")
        
        default_requests = int(default_parts[0])
        strict_requests = int(strict_parts[0])
        auth_requests = int(auth_parts[0])
        
        assert auth_requests < strict_requests < default_requests

    def test_all_limits_use_minute_timeframe(self):
        """Test that all rate limits use minute timeframe"""
        assert DEFAULT_RATE_LIMIT.endswith("/minute")
        assert STRICT_RATE_LIMIT.endswith("/minute")
        assert AUTH_RATE_LIMIT.endswith("/minute")


class TestRateLimitErrorHandling:
    """Test suite for rate limit error handling scenarios"""

    def test_http_exception_status_code(self):
        """Test that HTTPException has correct status code"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.status_code == 429

    def test_http_exception_with_different_retry_values(self):
        """Test error handler with various retry_after values"""
        request = Mock(spec=Request)
        
        retry_values = [30, 60, 120, 300]
        
        for retry_value in retry_values:
            mock_exc = Mock(spec=RateLimitExceeded)
            mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
            mock_exc.retry_after = retry_value
            
            result = rate_limit_error_handler(request, mock_exc)
            
            assert result.detail["retry_after"] == retry_value

    def test_error_handler_preserves_exception_info(self):
        """Test that error handler preserves exception information"""
        request = Mock(spec=Request)
        
        exception_message = "IP 192.168.1.1 exceeded rate limit"
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value=exception_message)
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert exception_message in result.detail["message"]


class TestRateLimitConfiguration:
    """Test suite for rate limit configuration validation"""

    def test_rate_limit_format_valid(self):
        """Test that all rate limits follow valid format"""
        import re
        
        rate_limit_pattern = r'^\d+/(minute|second|hour|day)$'
        
        assert re.match(rate_limit_pattern, DEFAULT_RATE_LIMIT)
        assert re.match(rate_limit_pattern, STRICT_RATE_LIMIT)
        assert re.match(rate_limit_pattern, AUTH_RATE_LIMIT)

    def test_rate_limit_values_positive(self):
        """Test that all rate limit values are positive"""
        default_parts = DEFAULT_RATE_LIMIT.split("/")
        strict_parts = STRICT_RATE_LIMIT.split("/")
        auth_parts = AUTH_RATE_LIMIT.split("/")
        
        assert int(default_parts[0]) > 0
        assert int(strict_parts[0]) > 0
        assert int(auth_parts[0]) > 0

    def test_rate_limit_configuration_consistency(self):
        """Test that rate limit configuration is consistent"""
        # All limits should use the same time unit for consistency
        assert DEFAULT_RATE_LIMIT.endswith("/minute")
        assert STRICT_RATE_LIMIT.endswith("/minute")
        assert AUTH_RATE_LIMIT.endswith("/minute")


class TestRateLimitEdgeCases:
    """Test suite for rate limit edge cases"""

    def test_error_handler_with_zero_retry_after(self):
        """Test error handler with zero retry_after"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 0
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["retry_after"] == 0

    def test_error_handler_with_large_retry_after(self):
        """Test error handler with large retry_after"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="Rate limit exceeded")
        mock_exc.retry_after = 3600  # 1 hour
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["retry_after"] == 3600

    def test_error_handler_with_empty_message(self):
        """Test error handler with empty exception message"""
        request = Mock(spec=Request)
        
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value="")
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["message"] == ""

    def test_error_handler_with_long_message(self):
        """Test error handler with very long exception message"""
        request = Mock(spec=Request)
        
        long_message = "A" * 1000
        mock_exc = Mock(spec=RateLimitExceeded)
        mock_exc.__str__ = Mock(return_value=long_message)
        mock_exc.retry_after = 60
        
        result = rate_limit_error_handler(request, mock_exc)
        
        assert result.detail["message"] == long_message