import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.exceptions import (
    DomainException,
    ProductNotFoundException,
    ProductSKUAlreadyExistsException,
    CustomerNotFoundException,
    CustomerEmailAlreadyExistsException,
    OrderNotFoundException,
    InsufficientInventoryException
)


class TestDomainException:
    """Test suite for base DomainException"""

    def test_domain_exception_is_exception(self):
        """Test that DomainException inherits from Exception"""
        assert issubclass(DomainException, Exception)

    def test_domain_exception_can_be_raised(self):
        """Test that DomainException can be raised and caught"""
        with pytest.raises(DomainException):
            raise DomainException("Test error")

    def test_domain_exception_message(self):
        """Test that DomainException preserves error message"""
        error_message = "Test domain error"
        with pytest.raises(DomainException) as exc_info:
            raise DomainException(error_message)
        assert str(exc_info.value) == error_message


class TestProductNotFoundException:
    """Test suite for ProductNotFoundException"""

    def test_product_not_found_exception_is_domain_exception(self):
        """Test that ProductNotFoundException inherits from DomainException"""
        assert issubclass(ProductNotFoundException, DomainException)

    def test_product_not_found_exception_can_be_raised(self):
        """Test that ProductNotFoundException can be raised and caught"""
        with pytest.raises(ProductNotFoundException):
            raise ProductNotFoundException("Product not found")

    def test_product_not_found_exception_message(self):
        """Test that ProductNotFoundException preserves error message"""
        error_message = "Product with ID 999 not found"
        with pytest.raises(ProductNotFoundException) as exc_info:
            raise ProductNotFoundException(error_message)
        assert str(exc_info.value) == error_message

    def test_product_not_found_exception_with_id(self):
        """Test creating ProductNotFoundException with specific ID"""
        product_id = 123
        with pytest.raises(ProductNotFoundException) as exc_info:
            raise ProductNotFoundException(f"Product with ID {product_id} not found")
        assert str(product_id) in str(exc_info.value)


class TestProductSKUAlreadyExistsException:
    """Test suite for ProductSKUAlreadyExistsException"""

    def test_product_sku_already_exists_exception_is_domain_exception(self):
        """Test that ProductSKUAlreadyExistsException inherits from DomainException"""
        assert issubclass(ProductSKUAlreadyExistsException, DomainException)

    def test_product_sku_already_exists_exception_can_be_raised(self):
        """Test that ProductSKUAlreadyExistsException can be raised and caught"""
        with pytest.raises(ProductSKUAlreadyExistsException):
            raise ProductSKUAlreadyExistsException("SKU already exists")

    def test_product_sku_already_exists_exception_message(self):
        """Test that ProductSKUAlreadyExistsException preserves error message"""
        error_message = "Product with SKU TEST-001 already exists"
        with pytest.raises(ProductSKUAlreadyExistsException) as exc_info:
            raise ProductSKUAlreadyExistsException(error_message)
        assert str(exc_info.value) == error_message

    def test_product_sku_already_exists_exception_with_sku(self):
        """Test creating ProductSKUAlreadyExistsException with specific SKU"""
        sku = "TEST-001"
        with pytest.raises(ProductSKUAlreadyExistsException) as exc_info:
            raise ProductSKUAlreadyExistsException(f"Product with SKU {sku} already exists")
        assert sku in str(exc_info.value)


class TestCustomerNotFoundException:
    """Test suite for CustomerNotFoundException"""

    def test_customer_not_found_exception_is_domain_exception(self):
        """Test that CustomerNotFoundException inherits from DomainException"""
        assert issubclass(CustomerNotFoundException, DomainException)

    def test_customer_not_found_exception_can_be_raised(self):
        """Test that CustomerNotFoundException can be raised and caught"""
        with pytest.raises(CustomerNotFoundException):
            raise CustomerNotFoundException("Customer not found")

    def test_customer_not_found_exception_message(self):
        """Test that CustomerNotFoundException preserves error message"""
        error_message = "Customer with ID 999 not found"
        with pytest.raises(CustomerNotFoundException) as exc_info:
            raise CustomerNotFoundException(error_message)
        assert str(exc_info.value) == error_message

    def test_customer_not_found_exception_with_id(self):
        """Test creating CustomerNotFoundException with specific ID"""
        customer_id = 456
        with pytest.raises(CustomerNotFoundException) as exc_info:
            raise CustomerNotFoundException(f"Customer with ID {customer_id} not found")
        assert str(customer_id) in str(exc_info.value)


class TestCustomerEmailAlreadyExistsException:
    """Test suite for CustomerEmailAlreadyExistsException"""

    def test_customer_email_already_exists_exception_is_domain_exception(self):
        """Test that CustomerEmailAlreadyExistsException inherits from DomainException"""
        assert issubclass(CustomerEmailAlreadyExistsException, DomainException)

    def test_customer_email_already_exists_exception_can_be_raised(self):
        """Test that CustomerEmailAlreadyExistsException can be raised and caught"""
        with pytest.raises(CustomerEmailAlreadyExistsException):
            raise CustomerEmailAlreadyExistsException("Email already exists")

    def test_customer_email_already_exists_exception_message(self):
        """Test that CustomerEmailAlreadyExistsException preserves error message"""
        error_message = "Customer with email test@example.com already exists"
        with pytest.raises(CustomerEmailAlreadyExistsException) as exc_info:
            raise CustomerEmailAlreadyExistsException(error_message)
        assert str(exc_info.value) == error_message

    def test_customer_email_already_exists_exception_with_email(self):
        """Test creating CustomerEmailAlreadyExistsException with specific email"""
        email = "test@example.com"
        with pytest.raises(CustomerEmailAlreadyExistsException) as exc_info:
            raise CustomerEmailAlreadyExistsException(f"Customer with email {email} already exists")
        assert email in str(exc_info.value)


class TestOrderNotFoundException:
    """Test suite for OrderNotFoundException"""

    def test_order_not_found_exception_is_domain_exception(self):
        """Test that OrderNotFoundException inherits from DomainException"""
        assert issubclass(OrderNotFoundException, DomainException)

    def test_order_not_found_exception_can_be_raised(self):
        """Test that OrderNotFoundException can be raised and caught"""
        with pytest.raises(OrderNotFoundException):
            raise OrderNotFoundException("Order not found")

    def test_order_not_found_exception_message(self):
        """Test that OrderNotFoundException preserves error message"""
        error_message = "Order with ID 999 not found"
        with pytest.raises(OrderNotFoundException) as exc_info:
            raise OrderNotFoundException(error_message)
        assert str(exc_info.value) == error_message

    def test_order_not_found_exception_with_id(self):
        """Test creating OrderNotFoundException with specific ID"""
        order_id = 789
        with pytest.raises(OrderNotFoundException) as exc_info:
            raise OrderNotFoundException(f"Order with ID {order_id} not found")
        assert str(order_id) in str(exc_info.value)


class TestInsufficientInventoryException:
    """Test suite for InsufficientInventoryException"""

    def test_insufficient_inventory_exception_is_domain_exception(self):
        """Test that InsufficientInventoryException inherits from DomainException"""
        assert issubclass(InsufficientInventoryException, DomainException)

    def test_insufficient_inventory_exception_can_be_raised(self):
        """Test that InsufficientInventoryException can be raised and caught"""
        with pytest.raises(InsufficientInventoryException):
            raise InsufficientInventoryException("Insufficient inventory")

    def test_insufficient_inventory_exception_message(self):
        """Test that InsufficientInventoryException preserves error message"""
        error_message = "Insufficient inventory. Only 5 units available."
        with pytest.raises(InsufficientInventoryException) as exc_info:
            raise InsufficientInventoryException(error_message)
        assert str(exc_info.value) == error_message

    def test_insufficient_inventory_exception_with_quantity(self):
        """Test creating InsufficientInventoryException with specific quantity"""
        available_quantity = 5
        with pytest.raises(InsufficientInventoryException) as exc_info:
            raise InsufficientInventoryException(
                f"Insufficient inventory. Only {available_quantity} units available."
            )
        assert str(available_quantity) in str(exc_info.value)


class TestExceptionHierarchy:
    """Test suite for exception hierarchy and catching"""

    def test_catch_product_not_found_as_domain_exception(self):
        """Test that ProductNotFoundException can be caught as DomainException"""
        with pytest.raises(DomainException):
            raise ProductNotFoundException("Product not found")

    def test_catch_customer_not_found_as_domain_exception(self):
        """Test that CustomerNotFoundException can be caught as DomainException"""
        with pytest.raises(DomainException):
            raise CustomerNotFoundException("Customer not found")

    def test_catch_order_not_found_as_domain_exception(self):
        """Test that OrderNotFoundException can be caught as DomainException"""
        with pytest.raises(DomainException):
            raise OrderNotFoundException("Order not found")

    def test_catch_insufficient_inventory_as_domain_exception(self):
        """Test that InsufficientInventoryException can be caught as DomainException"""
        with pytest.raises(DomainException):
            raise InsufficientInventoryException("Insufficient inventory")

    def test_specific_exception_catch_over_generic(self):
        """Test that specific exceptions are caught before generic ones"""
        try:
            raise ProductNotFoundException("Product not found")
        except ProductNotFoundException:
            # Should be caught here
            caught = True
        except DomainException:
            # Should not reach here
            caught = False
        assert caught is True