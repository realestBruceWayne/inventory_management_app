from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Product, Customer, Order


class IProductRepository(ABC):
    """Interface for product data access operations"""

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Retrieve all products"""
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by ID"""
        pass

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Retrieve a product by SKU"""
        pass

    @abstractmethod
    def create(self, product: Product) -> Product:
        """Create a new product"""
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        """Update an existing product"""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete a product"""
        pass

    @abstractmethod
    def exists_by_sku(self, sku: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a product with the given SKU exists"""
        pass


class ICustomerRepository(ABC):
    """Interface for customer data access operations"""

    @abstractmethod
    def get_all(self) -> List[Customer]:
        """Retrieve all customers"""
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email"""
        pass

    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """Update an existing customer"""
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        """Delete a customer"""
        pass

    @abstractmethod
    def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a customer with the given email exists"""
        pass


class IOrderRepository(ABC):
    """Interface for order data access operations"""

    @abstractmethod
    def get_all(self) -> List[Order]:
        """Retrieve all orders"""
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by ID"""
        pass

    @abstractmethod
    def create(self, order: Order) -> Order:
        """Create a new order"""
        pass

    @abstractmethod
    def delete(self, order_id: int) -> bool:
        """Delete an order"""
        pass
