import pytest
import sys
import os
from unittest.mock import Mock, call

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService
from domain.entities import Product, Customer, Order
from domain.exceptions import (
    ProductNotFoundException,
    ProductSKUAlreadyExistsException,
    CustomerNotFoundException,
    CustomerEmailAlreadyExistsException,
    OrderNotFoundException,
    InsufficientInventoryException
)


class TestProductService:
    """Test suite for ProductService"""

    def test_get_all_products(self, mock_product_repository, sample_products):
        """Test retrieving all products"""
        mock_product_repository.get_all.return_value = sample_products
        service = ProductService(mock_product_repository)
        
        products = service.get_all_products()
        
        assert len(products) == 3
        mock_product_repository.get_all.assert_called_once()

    def test_get_all_products_empty(self, mock_product_repository):
        """Test retrieving all products when none exist"""
        mock_product_repository.get_all.return_value = []
        service = ProductService(mock_product_repository)
        
        products = service.get_all_products()
        
        assert len(products) == 0
        mock_product_repository.get_all.assert_called_once()

    def test_get_product_by_id_success(self, mock_product_repository, sample_product):
        """Test retrieving a product by ID successfully"""
        mock_product_repository.get_by_id.return_value = sample_product
        service = ProductService(mock_product_repository)
        
        product = service.get_product_by_id(1)
        
        assert product.id == 1
        assert product.name == "Test Product"
        mock_product_repository.get_by_id.assert_called_once_with(1)

    def test_get_product_by_id_not_found(self, mock_product_repository):
        """Test retrieving a product by ID when not found"""
        mock_product_repository.get_by_id.return_value = None
        service = ProductService(mock_product_repository)
        
        with pytest.raises(ProductNotFoundException, match="Product with ID 999 not found"):
            service.get_product_by_id(999)
        
        mock_product_repository.get_by_id.assert_called_once_with(999)

    def test_create_product_success(self, mock_product_repository, sample_product):
        """Test creating a product successfully"""
        mock_product_repository.exists_by_sku.return_value = False
        mock_product_repository.create.return_value = sample_product
        service = ProductService(mock_product_repository)
        
        new_product = Product(name="New Product", sku="NEW-001", price=29.99, quantity=10)
        created_product = service.create_product(new_product)
        
        assert created_product.id == 1
        mock_product_repository.exists_by_sku.assert_called_once_with("NEW-001")
        mock_product_repository.create.assert_called_once_with(new_product)

    def test_create_product_sku_exists(self, mock_product_repository):
        """Test creating a product when SKU already exists"""
        mock_product_repository.exists_by_sku.return_value = True
        service = ProductService(mock_product_repository)
        
        new_product = Product(name="New Product", sku="EXISTING-001", price=29.99, quantity=10)
        
        with pytest.raises(ProductSKUAlreadyExistsException, match="Product with SKU EXISTING-001 already exists"):
            service.create_product(new_product)
        
        mock_product_repository.exists_by_sku.assert_called_once_with("EXISTING-001")
        mock_product_repository.create.assert_not_called()

    def test_update_product_success(self, mock_product_repository, sample_product):
        """Test updating a product successfully"""
        mock_product_repository.get_by_id.return_value = sample_product
        mock_product_repository.exists_by_sku.return_value = False
        mock_product_repository.update.return_value = sample_product
        service = ProductService(mock_product_repository)
        
        updated_product = Product(name="Updated Product", sku="TEST-001", price=149.99, quantity=40)
        result = service.update_product(1, updated_product)
        
        assert result.id == 1
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.exists_by_sku.assert_called_once_with("TEST-001", exclude_id=1)
        mock_product_repository.update.assert_called_once()

    def test_update_product_not_found(self, mock_product_repository):
        """Test updating a product when not found"""
        mock_product_repository.get_by_id.return_value = None
        service = ProductService(mock_product_repository)
        
        updated_product = Product(name="Updated Product", sku="TEST-001", price=149.99, quantity=40)
        
        with pytest.raises(ProductNotFoundException, match="Product with ID 999 not found"):
            service.update_product(999, updated_product)
        
        mock_product_repository.get_by_id.assert_called_once_with(999)
        mock_product_repository.exists_by_sku.assert_not_called()
        mock_product_repository.update.assert_not_called()

    def test_update_product_sku_exists(self, mock_product_repository, sample_product):
        """Test updating a product when SKU already exists for another product"""
        mock_product_repository.get_by_id.return_value = sample_product
        mock_product_repository.exists_by_sku.return_value = True
        service = ProductService(mock_product_repository)
        
        updated_product = Product(name="Updated Product", sku="EXISTING-002", price=149.99, quantity=40)
        
        with pytest.raises(ProductSKUAlreadyExistsException, match="Product with SKU EXISTING-002 already exists"):
            service.update_product(1, updated_product)
        
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.exists_by_sku.assert_called_once_with("EXISTING-002", exclude_id=1)
        mock_product_repository.update.assert_not_called()

    def test_delete_product_success(self, mock_product_repository, sample_product):
        """Test deleting a product successfully"""
        mock_product_repository.get_by_id.return_value = sample_product
        mock_product_repository.delete.return_value = True
        service = ProductService(mock_product_repository)
        
        service.delete_product(1)
        
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.delete.assert_called_once_with(1)

    def test_delete_product_not_found(self, mock_product_repository):
        """Test deleting a product when not found"""
        mock_product_repository.get_by_id.return_value = None
        service = ProductService(mock_product_repository)
        
        with pytest.raises(ProductNotFoundException, match="Product with ID 999 not found"):
            service.delete_product(999)
        
        mock_product_repository.get_by_id.assert_called_once_with(999)
        mock_product_repository.delete.assert_not_called()

    def test_get_low_stock_products(self, mock_product_repository, sample_products):
        """Test retrieving products with low stock"""
        mock_product_repository.get_all.return_value = sample_products
        service = ProductService(mock_product_repository)
        
        low_stock_products = service.get_low_stock_products(threshold=10)
        
        assert len(low_stock_products) == 1
        assert low_stock_products[0].id == 3
        assert low_stock_products[0].quantity == 5
        mock_product_repository.get_all.assert_called_once()

    def test_get_low_stock_products_default_threshold(self, mock_product_repository, sample_products):
        """Test retrieving low stock products with default threshold"""
        mock_product_repository.get_all.return_value = sample_products
        service = ProductService(mock_product_repository)
        
        low_stock_products = service.get_low_stock_products()
        
        assert len(low_stock_products) == 1
        mock_product_repository.get_all.assert_called_once()

    def test_get_low_stock_products_none(self, mock_product_repository, sample_products):
        """Test retrieving low stock products when none are low stock"""
        # All products have sufficient stock
        high_stock_products = [
            Product(id=1, name="Product A", sku="SKU-001", price=10.0, quantity=100),
            Product(id=2, name="Product B", sku="SKU-002", price=20.0, quantity=50),
        ]
        mock_product_repository.get_all.return_value = high_stock_products
        service = ProductService(mock_product_repository)
        
        low_stock_products = service.get_low_stock_products(threshold=10)
        
        assert len(low_stock_products) == 0


class TestCustomerService:
    """Test suite for CustomerService"""

    def test_get_all_customers(self, mock_customer_repository, sample_customers):
        """Test retrieving all customers"""
        mock_customer_repository.get_all.return_value = sample_customers
        service = CustomerService(mock_customer_repository)
        
        customers = service.get_all_customers()
        
        assert len(customers) == 2
        mock_customer_repository.get_all.assert_called_once()

    def test_get_all_customers_empty(self, mock_customer_repository):
        """Test retrieving all customers when none exist"""
        mock_customer_repository.get_all.return_value = []
        service = CustomerService(mock_customer_repository)
        
        customers = service.get_all_customers()
        
        assert len(customers) == 0
        mock_customer_repository.get_all.assert_called_once()

    def test_get_customer_by_id_success(self, mock_customer_repository, sample_customer):
        """Test retrieving a customer by ID successfully"""
        mock_customer_repository.get_by_id.return_value = sample_customer
        service = CustomerService(mock_customer_repository)
        
        customer = service.get_customer_by_id(1)
        
        assert customer.id == 1
        assert customer.full_name == "John Doe"
        mock_customer_repository.get_by_id.assert_called_once_with(1)

    def test_get_customer_by_id_not_found(self, mock_customer_repository):
        """Test retrieving a customer by ID when not found"""
        mock_customer_repository.get_by_id.return_value = None
        service = CustomerService(mock_customer_repository)
        
        with pytest.raises(CustomerNotFoundException, match="Customer with ID 999 not found"):
            service.get_customer_by_id(999)
        
        mock_customer_repository.get_by_id.assert_called_once_with(999)

    def test_create_customer_success(self, mock_customer_repository, sample_customer):
        """Test creating a customer successfully"""
        mock_customer_repository.exists_by_email.return_value = False
        mock_customer_repository.create.return_value = sample_customer
        service = CustomerService(mock_customer_repository)
        
        new_customer = Customer(full_name="Jane Doe", email="jane.doe@example.com", phone="+9876543210")
        created_customer = service.create_customer(new_customer)
        
        assert created_customer.id == 1
        mock_customer_repository.exists_by_email.assert_called_once_with("jane.doe@example.com")
        mock_customer_repository.create.assert_called_once_with(new_customer)

    def test_create_customer_email_exists(self, mock_customer_repository):
        """Test creating a customer when email already exists"""
        mock_customer_repository.exists_by_email.return_value = True
        service = CustomerService(mock_customer_repository)
        
        new_customer = Customer(full_name="Jane Doe", email="existing@example.com", phone="+9876543210")
        
        with pytest.raises(CustomerEmailAlreadyExistsException, match="Customer with email existing@example.com already exists"):
            service.create_customer(new_customer)
        
        mock_customer_repository.exists_by_email.assert_called_once_with("existing@example.com")
        mock_customer_repository.create.assert_not_called()

    def test_delete_customer_success(self, mock_customer_repository, sample_customer):
        """Test deleting a customer successfully"""
        mock_customer_repository.get_by_id.return_value = sample_customer
        mock_customer_repository.delete.return_value = True
        service = CustomerService(mock_customer_repository)
        
        service.delete_customer(1)
        
        mock_customer_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.delete.assert_called_once_with(1)

    def test_delete_customer_not_found(self, mock_customer_repository):
        """Test deleting a customer when not found"""
        mock_customer_repository.get_by_id.return_value = None
        service = CustomerService(mock_customer_repository)
        
        with pytest.raises(CustomerNotFoundException, match="Customer with ID 999 not found"):
            service.delete_customer(999)
        
        mock_customer_repository.get_by_id.assert_called_once_with(999)
        mock_customer_repository.delete.assert_not_called()

    def test_update_customer_success(self, mock_customer_repository, sample_customer):
        """Test updating a customer successfully"""
        mock_customer_repository.get_by_id.return_value = sample_customer
        mock_customer_repository.exists_by_email.return_value = False
        mock_customer_repository.update.return_value = sample_customer
        service = CustomerService(mock_customer_repository)
        
        updated_customer = Customer(full_name="Jane Doe", email="john.doe@example.com", phone="+9999999999")
        result = service.update_customer(1, updated_customer)
        
        assert result.id == 1
        mock_customer_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.exists_by_email.assert_called_once_with("john.doe@example.com", exclude_id=1)
        mock_customer_repository.update.assert_called_once()

    def test_update_customer_not_found(self, mock_customer_repository):
        """Test updating a customer when not found"""
        mock_customer_repository.get_by_id.return_value = None
        service = CustomerService(mock_customer_repository)
        
        updated_customer = Customer(full_name="Jane Doe", email="jane.doe@example.com", phone="+9999999999")
        
        with pytest.raises(CustomerNotFoundException, match="Customer with ID 999 not found"):
            service.update_customer(999, updated_customer)
        
        mock_customer_repository.get_by_id.assert_called_once_with(999)
        mock_customer_repository.exists_by_email.assert_not_called()
        mock_customer_repository.update.assert_not_called()

    def test_update_customer_email_exists(self, mock_customer_repository, sample_customer):
        """Test updating a customer when email already exists for another customer"""
        mock_customer_repository.get_by_id.return_value = sample_customer
        mock_customer_repository.exists_by_email.return_value = True
        service = CustomerService(mock_customer_repository)
        
        updated_customer = Customer(full_name="Jane Doe", email="existing@example.com", phone="+9999999999")
        
        with pytest.raises(CustomerEmailAlreadyExistsException, match="Customer with email existing@example.com already exists"):
            service.update_customer(1, updated_customer)
        
        mock_customer_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.exists_by_email.assert_called_once_with("existing@example.com", exclude_id=1)
        mock_customer_repository.update.assert_not_called()


class TestOrderService:
    """Test suite for OrderService"""

    def test_get_all_orders(self, mock_order_repository, sample_orders):
        """Test retrieving all orders"""
        mock_order_repository.get_all.return_value = sample_orders
        service = OrderService(mock_order_repository, Mock(), Mock())
        
        orders = service.get_all_orders()
        
        assert len(orders) == 2
        mock_order_repository.get_all.assert_called_once()

    def test_get_all_orders_empty(self, mock_order_repository):
        """Test retrieving all orders when none exist"""
        mock_order_repository.get_all.return_value = []
        service = OrderService(mock_order_repository, Mock(), Mock())
        
        orders = service.get_all_orders()
        
        assert len(orders) == 0
        mock_order_repository.get_all.assert_called_once()

    def test_get_order_by_id_success(self, mock_order_repository, sample_order):
        """Test retrieving an order by ID successfully"""
        mock_order_repository.get_by_id.return_value = sample_order
        service = OrderService(mock_order_repository, Mock(), Mock())
        
        order = service.get_order_by_id(1)
        
        assert order.id == 1
        mock_order_repository.get_by_id.assert_called_once_with(1)

    def test_get_order_by_id_not_found(self, mock_order_repository):
        """Test retrieving an order by ID when not found"""
        mock_order_repository.get_by_id.return_value = None
        service = OrderService(mock_order_repository, Mock(), Mock())
        
        with pytest.raises(OrderNotFoundException, match="Order with ID 999 not found"):
            service.get_order_by_id(999)
        
        mock_order_repository.get_by_id.assert_called_once_with(999)

    def test_create_order_success(self, mock_order_repository, mock_product_repository, mock_customer_repository, sample_product, sample_customer):
        """Test creating an order successfully"""
        mock_product_repository.get_by_id.return_value = sample_product
        mock_customer_repository.get_by_id.return_value = sample_customer
        mock_order_repository.create.return_value = sample_order = Order(
            id=1, customer_id=1, product_id=1, quantity=5, total_amount=499.95
        )
        service = OrderService(mock_order_repository, mock_product_repository, mock_customer_repository)
        
        new_order = Order(customer_id=1, product_id=1, quantity=5, total_amount=0.0)
        created_order = service.create_order(new_order)
        
        assert created_order.id == 1
        assert created_order.total_amount == 499.95
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.update.assert_called_once()
        mock_order_repository.create.assert_called_once()

    def test_create_order_product_not_found(self, mock_order_repository, mock_product_repository, mock_customer_repository):
        """Test creating an order when product doesn't exist"""
        mock_product_repository.get_by_id.return_value = None
        service = OrderService(mock_order_repository, mock_product_repository, mock_customer_repository)
        
        new_order = Order(customer_id=1, product_id=999, quantity=5, total_amount=0.0)
        
        with pytest.raises(ProductNotFoundException, match="Product with ID 999 not found"):
            service.create_order(new_order)
        
        mock_product_repository.get_by_id.assert_called_once_with(999)
        mock_customer_repository.get_by_id.assert_not_called()
        mock_order_repository.create.assert_not_called()

    def test_create_order_customer_not_found(self, mock_order_repository, mock_product_repository, mock_customer_repository, sample_product):
        """Test creating an order when customer doesn't exist"""
        mock_product_repository.get_by_id.return_value = sample_product
        mock_customer_repository.get_by_id.return_value = None
        service = OrderService(mock_order_repository, mock_product_repository, mock_customer_repository)
        
        new_order = Order(customer_id=999, product_id=1, quantity=5, total_amount=0.0)
        
        with pytest.raises(CustomerNotFoundException, match="Customer with ID 999 not found"):
            service.create_order(new_order)
        
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.get_by_id.assert_called_once_with(999)
        mock_order_repository.create.assert_not_called()

    def test_create_order_insufficient_inventory(self, mock_order_repository, mock_product_repository, mock_customer_repository, sample_product, sample_customer):
        """Test creating an order when inventory is insufficient"""
        low_stock_product = Product(id=1, name="Test", sku="TEST-001", price=99.99, quantity=2)
        mock_product_repository.get_by_id.return_value = low_stock_product
        mock_customer_repository.get_by_id.return_value = sample_customer
        service = OrderService(mock_order_repository, mock_product_repository, mock_customer_repository)
        
        new_order = Order(customer_id=1, product_id=1, quantity=5, total_amount=0.0)
        
        with pytest.raises(InsufficientInventoryException, match="Insufficient inventory. Only 2 units available."):
            service.create_order(new_order)
        
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_customer_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.update.assert_not_called()
        mock_order_repository.create.assert_not_called()

    def test_delete_order_success(self, mock_order_repository, mock_product_repository, sample_order, sample_product):
        """Test deleting an order successfully and restoring inventory"""
        mock_order_repository.get_by_id.return_value = sample_order
        mock_product_repository.get_by_id.return_value = sample_product
        mock_order_repository.delete.return_value = True
        service = OrderService(mock_order_repository, mock_product_repository, Mock())
        
        service.delete_order(1)
        
        mock_order_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.update.assert_called_once()
        mock_order_repository.delete.assert_called_once_with(1)

    def test_delete_order_not_found(self, mock_order_repository, mock_product_repository):
        """Test deleting an order when not found"""
        mock_order_repository.get_by_id.return_value = None
        service = OrderService(mock_order_repository, mock_product_repository, Mock())
        
        with pytest.raises(OrderNotFoundException, match="Order with ID 999 not found"):
            service.delete_order(999)
        
        mock_order_repository.get_by_id.assert_called_once_with(999)
        mock_product_repository.get_by_id.assert_not_called()
        mock_product_repository.update.assert_not_called()
        mock_order_repository.delete.assert_not_called()

    def test_delete_order_product_not_found(self, mock_order_repository, mock_product_repository, sample_order):
        """Test deleting an order when product doesn't exist (should still delete order)"""
        mock_order_repository.get_by_id.return_value = sample_order
        mock_product_repository.get_by_id.return_value = None
        mock_order_repository.delete.return_value = True
        service = OrderService(mock_order_repository, mock_product_repository, Mock())
        
        service.delete_order(1)
        
        mock_order_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.update.assert_not_called()
        mock_order_repository.delete.assert_called_once_with(1)