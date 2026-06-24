import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import Product, Customer, Order


class TestProduct:
    """Test suite for Product entity"""

    def test_product_creation_valid(self):
        """Test creating a product with valid data"""
        product = Product(
            id=1,
            name="Test Product",
            sku="TEST-001",
            price=99.99,
            quantity=50
        )
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.sku == "TEST-001"
        assert product.price == 99.99
        assert product.quantity == 50

    def test_product_creation_defaults(self):
        """Test creating a product with default values"""
        product = Product()
        assert product.id is None
        assert product.name == ""
        assert product.sku == ""
        assert product.price == 0.0
        assert product.quantity == 0

    def test_product_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError"""
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            Product(name="Test", sku="TEST-001", price=10.0, quantity=-5)

    def test_product_negative_price_raises_error(self):
        """Test that negative price raises ValueError"""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product(name="Test", sku="TEST-001", price=-10.0, quantity=10)

    def test_product_decrease_quantity_valid(self):
        """Test decreasing quantity with valid amount"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=20)
        product.decrease_quantity(5)
        assert product.quantity == 15

    def test_product_decrease_quantity_insufficient(self):
        """Test that decreasing quantity below available raises ValueError"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=10)
        with pytest.raises(ValueError, match="Insufficient quantity"):
            product.decrease_quantity(15)

    def test_product_increase_quantity_valid(self):
        """Test increasing quantity with valid amount"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=10)
        product.increase_quantity(5)
        assert product.quantity == 15

    def test_product_increase_quantity_negative_amount(self):
        """Test that increasing quantity with negative amount raises ValueError"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=10)
        with pytest.raises(ValueError, match="Amount must be positive"):
            product.increase_quantity(-5)

    def test_product_is_low_stock_true(self):
        """Test that product is correctly identified as low stock"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=5)
        assert product.is_low_stock(threshold=10) is True

    def test_product_is_low_stock_false(self):
        """Test that product is correctly identified as not low stock"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=20)
        assert product.is_low_stock(threshold=10) is False

    def test_product_is_low_stock_equal_threshold(self):
        """Test that product at threshold is considered low stock"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=10)
        assert product.is_low_stock(threshold=10) is True

    def test_product_is_low_stock_default_threshold(self):
        """Test that default threshold of 10 is used"""
        product = Product(id=1, name="Test", sku="TEST-001", price=10.0, quantity=10)
        assert product.is_low_stock() is True


class TestCustomer:
    """Test suite for Customer entity"""

    def test_customer_creation_valid(self):
        """Test creating a customer with valid data"""
        customer = Customer(
            id=1,
            full_name="John Doe",
            email="john.doe@example.com",
            phone="+1234567890"
        )
        assert customer.id == 1
        assert customer.full_name == "John Doe"
        assert customer.email == "john.doe@example.com"
        assert customer.phone == "+1234567890"

    def test_customer_creation_defaults(self):
        """Test creating a customer with default values"""
        customer = Customer()
        assert customer.id is None
        assert customer.full_name == ""
        assert customer.email == ""
        assert customer.phone is None

    def test_customer_creation_without_phone(self):
        """Test creating a customer without phone number"""
        customer = Customer(
            id=1,
            full_name="John Doe",
            email="john.doe@example.com"
        )
        assert customer.phone is None

    def test_customer_invalid_email_format(self):
        """Test that invalid email format raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Customer(full_name="John Doe", email="invalid-email")

    def test_customer_empty_email(self):
        """Test that empty email raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Customer(full_name="John Doe", email="")

    def test_customer_missing_at_symbol(self):
        """Test that email without @ symbol raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Customer(full_name="John Doe", email="invalid.com")


class TestOrder:
    """Test suite for Order entity"""

    def test_order_creation_valid(self):
        """Test creating an order with valid data"""
        order = Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=5,
            total_amount=99.95,
            created_at=datetime.now()
        )
        assert order.id == 1
        assert order.customer_id == 1
        assert order.product_id == 1
        assert order.quantity == 5
        assert order.total_amount == 99.95
        assert order.created_at is not None

    def test_order_creation_defaults(self):
        """Test creating an order with default values"""
        order = Order()
        assert order.id is None
        assert order.customer_id == 0
        assert order.product_id == 0
        assert order.quantity == 0
        assert order.total_amount == 0.0
        assert order.created_at is None

    def test_order_creation_without_created_at(self):
        """Test creating an order without created_at timestamp"""
        order = Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=5,
            total_amount=99.95
        )
        assert order.created_at is None

    def test_order_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError"""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Order(customer_id=1, product_id=1, quantity=-5, total_amount=0.0)

    def test_order_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError"""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Order(customer_id=1, product_id=1, quantity=0, total_amount=0.0)

    def test_order_negative_total_amount_raises_error(self):
        """Test that negative total amount raises ValueError"""
        with pytest.raises(ValueError, match="Total amount cannot be negative"):
            Order(customer_id=1, product_id=1, quantity=5, total_amount=-99.95)

    def test_order_calculate_total(self):
        """Test calculating total amount based on product price"""
        order = Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=5,
            total_amount=0.0
        )
        order.calculate_total(19.99)
        assert order.total_amount == 99.95

    def test_order_calculate_total_zero_quantity(self):
        """Test calculating total with zero quantity (should still work if validation disabled)"""
        order = Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=0,
            total_amount=0.0
        )
        # This test verifies the calculation logic even if validation would prevent this state
        order.quantity = 0  # Bypass validation for testing calculation
        order.calculate_total(19.99)
        assert order.total_amount == 0.0

    def test_order_calculate_total_expensive_product(self):
        """Test calculating total with expensive product"""
        order = Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=10,
            total_amount=0.0
        )
        order.calculate_total(999.99)
        assert order.total_amount == 9999.9