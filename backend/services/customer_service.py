from typing import List, Optional
from repositories.interfaces import ICustomerRepository
from domain.entities import Customer
from domain.exceptions import (
    CustomerNotFoundException,
    CustomerEmailAlreadyExistsException,
)


class CustomerService:
    """Service for customer business logic following Single Responsibility Principle"""

    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def get_all_customers(self) -> List[Customer]:
        """Retrieve all customers"""
        return self.customer_repository.get_all()

    def get_customer_by_id(self, customer_id: int) -> Customer:
        """Retrieve a customer by ID"""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(f"Customer with ID {customer_id} not found")
        return customer

    def create_customer(self, customer: Customer) -> Customer:
        """Create a new customer"""
        if self.customer_repository.exists_by_email(customer.email):
            raise CustomerEmailAlreadyExistsException(f"Customer with email {customer.email} already exists")
        return self.customer_repository.create(customer)

    def delete_customer(self, customer_id: int) -> None:
        """Delete a customer"""
        if not self.customer_repository.get_by_id(customer_id):
            raise CustomerNotFoundException(f"Customer with ID {customer_id} not found")
        self.customer_repository.delete(customer_id)

    def update_customer(self, customer_id: int, customer: Customer) -> Customer:
        """Update an existing customer"""
        existing_customer = self.customer_repository.get_by_id(customer_id)
        if not existing_customer:
            raise CustomerNotFoundException(f"Customer with ID {customer_id} not found")

        if self.customer_repository.exists_by_email(customer.email, exclude_id=customer_id):
            raise CustomerEmailAlreadyExistsException(f"Customer with email {customer.email} already exists")

        customer.id = customer_id
        return self.customer_repository.update(customer)
