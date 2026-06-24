import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from jose import JWTError
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
import sys
sys.path.insert(0, '/home/himanshu/repos/ethara_ai/backend')
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    get_current_user,
    verify_api_key,
    get_api_key_user
)


class TestPasswordHashing:
    """Test suite for password hashing and verification"""

    def test_get_password_hash(self):
        """Test that password hashing generates a hash"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 20  # Bcrypt hashes are typically 60 characters
        assert hashed.startswith("$2b$")  # Bcrypt hash prefix

    def test_verify_password_correct(self):
        """Test verifying a correct password"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying an incorrect password"""
        password = "test_password_123"
        wrong_password = "wrong_password_456"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self):
        """Test verifying with empty password"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert verify_password("", hashed) is False

    def test_hash_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password_123"
        password2 = "password_456"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2

    def test_hash_same_password_different_hashes(self):
        """Test that hashing the same password twice produces different hashes (salt)"""
        password = "test_password_123"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Bcrypt uses salt, so hashes should be different
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestTokenCreation:
    """Test suite for JWT token creation"""

    def test_create_access_token_default_expiry(self):
        """Test creating a token with default expiration"""
        data = {"sub": "user123", "role": "admin"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 20  # JWT tokens are typically long strings

    def test_create_access_token_custom_expiry(self):
        """Test creating a token with custom expiration"""
        data = {"sub": "user123", "role": "admin"}
        custom_delta = timedelta(hours=2)
        token = create_access_token(data, expires_delta=custom_delta)
        
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_access_token_with_different_data(self):
        """Test creating tokens with different payload data"""
        data1 = {"sub": "user1", "role": "user"}
        data2 = {"sub": "user2", "role": "admin"}
        
        token1 = create_access_token(data1)
        token2 = create_access_token(data2)
        
        assert token1 != token2

    def test_create_access_token_includes_exp(self):
        """Test that token includes expiration claim"""
        data = {"sub": "user123"}
        token = create_access_token(data)
        
        # Decode token to check it has exp claim
        # We'll verify this through verify_token
        payload = verify_token(token)
        assert "exp" in payload
        assert payload["sub"] == "user123"


class TestTokenVerification:
    """Test suite for JWT token verification"""

    def test_verify_token_valid(self):
        """Test verifying a valid token"""
        data = {"sub": "user123", "role": "admin"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        
        assert payload["sub"] == "user123"
        assert payload["role"] == "admin"
        assert "exp" in payload

    def test_verify_token_invalid(self):
        """Test verifying an invalid token"""
        invalid_token = "invalid.token.string"
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(invalid_token)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_token_expired(self):
        """Test verifying an expired token"""
        data = {"sub": "user123"}
        # Create token that's already expired
        expired_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expired_delta)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_token_tampered(self):
        """Test verifying a tampered token"""
        data = {"sub": "user123"}
        token = create_access_token(data)
        
        # Tamper with the token by changing a character
        tampered_token = token[:-5] + "abcde"
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(tampered_token)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Test suite for get_current_user dependency"""

    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self):
        """Test getting current user with valid token"""
        data = {"sub": "user123", "role": "admin"}
        token = create_access_token(data)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        result = await get_current_user(credentials)
        
        assert result["sub"] == "user123"
        assert result["role"] == "admin"

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        invalid_token = "invalid.token.string"
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=invalid_token
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_get_current_user_expired_token(self):
        """Test getting current user with expired token"""
        data = {"sub": "user123"}
        expired_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expired_delta)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestAPIKeyAuthentication:
    """Test suite for API key authentication"""

    def test_verify_api_key_valid(self):
        """Test verifying a valid API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            assert verify_api_key("test-api-key-12345") is True

    def test_verify_api_key_invalid(self):
        """Test verifying an invalid API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            assert verify_api_key("wrong-api-key") is False

    def test_verify_api_key_default(self):
        """Test verifying API key with default value"""
        # When API_KEY env var is not set, it uses the default
        with patch.dict(os.environ, {}, clear=True):
            assert verify_api_key("your-api-key-change-this-in-production") is True

    def test_verify_api_key_empty(self):
        """Test verifying empty API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            assert verify_api_key("") is False

    @pytest.mark.asyncio
    async def test_get_api_key_user_valid(self):
        """Test getting user from valid API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            result = await get_api_key_user("test-api-key-12345")
            
            assert result["api_key"] == "test-api-key-12345"
            assert result["type"] == "api_key"

    @pytest.mark.asyncio
    async def test_get_api_key_user_invalid(self):
        """Test getting user from invalid API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            with pytest.raises(HTTPException) as exc_info:
                await get_api_key_user("wrong-api-key")
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid API Key" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_api_key_user_empty(self):
        """Test getting user from empty API key"""
        with patch.dict(os.environ, {"API_KEY": "test-api-key-12345"}):
            with pytest.raises(HTTPException) as exc_info:
                await get_api_key_user("")
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenExpiry:
    """Test suite for token expiration handling"""

    def test_token_expiry_future(self):
        """Test that token expiry is in the future"""
        data = {"sub": "user123"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        assert exp_timestamp > current_timestamp

    def test_token_expiry_custom_duration(self):
        """Test token expiry with custom duration"""
        data = {"sub": "user123"}
        custom_delta = timedelta(minutes=45)
        token = create_access_token(data, expires_delta=custom_delta)
        
        payload = verify_token(token)
        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        # Should be approximately 45 minutes in the future
        time_diff = exp_timestamp - current_timestamp
        assert 2700 < time_diff < 2710  # 45 minutes ± 10 seconds

    def test_token_expiry_short_duration(self):
        """Test token expiry with very short duration"""
        data = {"sub": "user123"}
        short_delta = timedelta(seconds=5)
        token = create_access_token(data, expires_delta=short_delta)
        
        payload = verify_token(token)
        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        # Should be approximately 5 seconds in the future
        time_diff = exp_timestamp - current_timestamp
        assert 4 < time_diff < 6  # 5 seconds ± 1 second


class TestSecurityConstants:
    """Test suite for security constants"""

    def test_secret_key_constant(self):
        """Test that SECRET_KEY is accessible"""
        from auth import SECRET_KEY
        assert isinstance(SECRET_KEY, str)
        assert len(SECRET_KEY) > 0

    def test_algorithm_constant(self):
        """Test that ALGORITHM is set correctly"""
        from auth import ALGORITHM
        assert ALGORITHM == "HS256"

    def test_access_token_expire_minutes(self):
        """Test that ACCESS_TOKEN_EXPIRE_MINUTES is set"""
        from auth import ACCESS_TOKEN_EXPIRE_MINUTES
        assert isinstance(ACCESS_TOKEN_EXPIRE_MINUTES, int)
        assert ACCESS_TOKEN_EXPIRE_MINUTES > 0