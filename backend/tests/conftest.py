import pytest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import Product, Customer, Order
from repositories.interfaces import IProductRepository, ICustomerRepository, IOrderRepository


@pytest.fixture
def mock_product_repository():
    """Create a mock product repository"""
    return Mock(spec=IProductRepository)


@pytest.fixture
def mock_customer_repository():
    """Create a mock customer repository"""
    return Mock(spec=ICustomerRepository)


@pytest.fixture
def mock_order_repository():
    """Create a mock order repository"""
    return Mock(spec=IOrderRepository)


@pytest.fixture
def sample_product():
    """Create a sample product for testing"""
    return Product(
        id=1,
        name="Test Product",
        sku="TEST-001",
        price=99.99,
        quantity=50
    )


@pytest.fixture
def sample_customer():
    """Create a sample customer for testing"""
    return Customer(
        id=1,
        full_name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890"
    )


@pytest.fixture
def sample_order():
    """Create a sample order for testing"""
    return Order(
        id=1,
        customer_id=1,
        product_id=1,
        quantity=5,
        total_amount=499.95,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_products():
    """Create a list of sample products for testing"""
    return [
        Product(id=1, name="Product A", sku="SKU-001", price=10.0, quantity=100),
        Product(id=2, name="Product B", sku="SKU-002", price=20.0, quantity=50),
        Product(id=3, name="Product C", sku="SKU-003", price=30.0, quantity=5),
    ]


@pytest.fixture
def sample_customers():
    """Create a list of sample customers for testing"""
    return [
        Customer(id=1, full_name="Alice Smith", email="alice@example.com", phone="+1111111111"),
        Customer(id=2, full_name="Bob Jones", email="bob@example.com", phone="+2222222222"),
    ]


@pytest.fixture
def sample_orders():
    """Create a list of sample orders for testing"""
    return [
        Order(id=1, customer_id=1, product_id=1, quantity=2, total_amount=20.0, created_at=datetime.now()),
        Order(id=2, customer_id=2, product_id=2, quantity=1, total_amount=20.0, created_at=datetime.now()),
    ]


@pytest.fixture
def low_stock_threshold():
    """Default low stock threshold"""
    return 10