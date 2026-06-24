from typing import List, Optional
from repositories.interfaces import IOrderRepository, IProductRepository, ICustomerRepository
from domain.entities import Order, Product, Customer
from domain.exceptions import (
    OrderNotFoundException,
    InsufficientInventoryException,
    ProductNotFoundException,
    CustomerNotFoundException,
)


class OrderService:
    """Service for order business logic following Single Responsibility Principle"""

    def __init__(self, order_repository: IOrderRepository, product_repository: IProductRepository, customer_repository: ICustomerRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def get_all_orders(self) -> List[Order]:
        """Retrieve all orders"""
        return self.order_repository.get_all()

    def get_order_by_id(self, order_id: int) -> Order:
        """Retrieve an order by ID"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Order with ID {order_id} not found")
        return order

    def create_order(self, order: Order) -> Order:
        """Create a new order with inventory validation"""
        # Validate product exists
        product = self.product_repository.get_by_id(order.product_id)
        if not product:
            raise ProductNotFoundException(f"Product with ID {order.product_id} not found")

        # Validate customer exists
        customer = self.customer_repository.get_by_id(order.customer_id)
        if not customer:
            raise CustomerNotFoundException(f"Customer with ID {order.customer_id} not found")

        # Check inventory
        if product.quantity < order.quantity:
            raise InsufficientInventoryException(
                f"Insufficient inventory. Only {product.quantity} units available."
            )

        # Calculate total amount
        order.calculate_total(product.price)

        # Decrease product quantity
        product.decrease_quantity(order.quantity)

        # Update product in repository
        self.product_repository.update(product)

        # Create order
        return self.order_repository.create(order)

    def delete_order(self, order_id: int) -> None:
        """Delete an order and restore inventory"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Order with ID {order_id} not found")

        # Restore inventory
        product = self.product_repository.get_by_id(order.product_id)
        if product:
            product.increase_quantity(order.quantity)
            self.product_repository.update(product)

        self.order_repository.delete(order_id)
