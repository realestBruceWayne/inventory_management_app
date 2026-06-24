from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories.sqlalchemy_repositories import (
    SQLAlchemyProductRepository,
    SQLAlchemyCustomerRepository,
    SQLAlchemyOrderRepository,
)
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService


def get_product_repository(db: Session = Depends(get_db)) -> SQLAlchemyProductRepository:
    """Dependency injection for product repository"""
    return SQLAlchemyProductRepository(db)


def get_customer_repository(db: Session = Depends(get_db)) -> SQLAlchemyCustomerRepository:
    """Dependency injection for customer repository"""
    return SQLAlchemyCustomerRepository(db)


def get_order_repository(db: Session = Depends(get_db)) -> SQLAlchemyOrderRepository:
    """Dependency injection for order repository"""
    return SQLAlchemyOrderRepository(db)


def get_product_service(
    product_repository: SQLAlchemyProductRepository = Depends(get_product_repository)
) -> ProductService:
    """Dependency injection for product service"""
    return ProductService(product_repository)


def get_customer_service(
    customer_repository: SQLAlchemyCustomerRepository = Depends(get_customer_repository)
) -> CustomerService:
    """Dependency injection for customer service"""
    return CustomerService(customer_repository)


def get_order_service(
    order_repository: SQLAlchemyOrderRepository = Depends(get_order_repository),
    product_repository: SQLAlchemyProductRepository = Depends(get_product_repository),
    customer_repository: SQLAlchemyCustomerRepository = Depends(get_customer_repository)
) -> OrderService:
    """Dependency injection for order service"""
    return OrderService(order_repository, product_repository, customer_repository)
