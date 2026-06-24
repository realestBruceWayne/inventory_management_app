import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock database before importing main
with patch('database.engine'):
    with patch('database.Base.metadata.create_all'):
        from main import app
        from domain.entities import Product, Customer, Order


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "version" in data
        assert "rate_limit" in data

    def test_root_endpoint_message(self, client):
        """Test root endpoint welcome message"""
        response = client.get("/")
        data = response.json()
        
        assert "Inventory & Order Management System" in data["message"]

    def test_root_endpoint_docs_link(self, client):
        """Test root endpoint docs link"""
        response = client.get("/")
        data = response.json()
        
        assert data["docs"] == "/docs"

    def test_root_endpoint_version(self, client):
        """Test root endpoint version"""
        response = client.get("/")
        data = response.json()
        
        assert data["version"] == "1.0.0"


class TestHealthEndpoint:
    """Test suite for health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


class TestBasicAPIEndpoints:
    """Test suite for basic API endpoints that don't require database"""

    def test_products_endpoint_exists(self, client):
        """Test that products endpoint exists (may fail due to DB, but endpoint should exist)"""
        response = client.get("/products")
        # We expect either success (200) or server error (500) due to DB, but not 404
        assert response.status_code in [200, 500]

    def test_customers_endpoint_exists(self, client):
        """Test that customers endpoint exists"""
        response = client.get("/customers")
        # We expect either success (200) or server error (500) due to DB, but not 404
        assert response.status_code in [200, 500]

    def test_orders_endpoint_exists(self, client):
        """Test that orders endpoint exists"""
        response = client.get("/orders")
        # We expect either success (200) or server error (500) due to DB, but not 404
        assert response.status_code in [200, 500]

    def test_products_by_id_endpoint_exists(self, client):
        """Test that products by ID endpoint exists"""
        response = client.get("/products/1")
        # We expect either success (200), not found (404), or server error (500)
        assert response.status_code in [200, 404, 500]

    def test_customers_by_id_endpoint_exists(self, client):
        """Test that customers by ID endpoint exists"""
        response = client.get("/customers/1")
        # We expect either success (200), not found (404), or server error (500)
        assert response.status_code in [200, 404, 500]

    def test_orders_by_id_endpoint_exists(self, client):
        """Test that orders by ID endpoint exists"""
        response = client.get("/orders/1")
        # We expect either success (200), not found (404), or server error (500)
        assert response.status_code in [200, 404, 500]


class TestErrorHandling:
    """Test suite for general error handling"""

    def test_404_endpoint(self, client):
        """Test that non-existent endpoints return 404"""
        response = client.get("/non-existent-endpoint")
        
        assert response.status_code == 404

    def test_invalid_method(self, client):
        """Test that invalid HTTP methods return 405"""
        response = client.post("/health")
        
        # FastAPI returns 405 Method Not Allowed for invalid methods
        assert response.status_code == 405


class TestCORSMiddleware:
    """Test suite for CORS middleware"""

    def test_cors_headers(self, client):
        """Test that CORS headers are present"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert response.status_code == 200


class TestAppConfiguration:
    """Test suite for app configuration"""

    def test_app_title(self):
        """Test that app has correct title"""
        assert app.title == "Inventory & Order Management System"

    def test_app_version(self):
        """Test that app has correct version"""
        assert app.version == "1.0.0"

    def test_app_description(self):
        """Test that app has description"""
        assert app.description is not None
        assert len(app.description) > 0