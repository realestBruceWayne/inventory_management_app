from typing import List, Optional
from sqlalchemy.orm import Session
from repositories.interfaces import IProductRepository, ICustomerRepository, IOrderRepository
from domain.entities import Product, Customer, Order
import models


class SQLAlchemyProductRepository(IProductRepository):
    """SQLAlchemy implementation of product repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        db_products = self.db.query(models.Product).all()
        return [
            Product(
                id=p.id,
                name=p.name,
                sku=p.sku,
                price=p.price,
                quantity=p.quantity,
            )
            for p in db_products
        ]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        db_product = self.db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return None
        return Product(
            id=db_product.id,
            name=db_product.name,
            sku=db_product.sku,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    def get_by_sku(self, sku: str) -> Optional[Product]:
        db_product = self.db.query(models.Product).filter(models.Product.sku == sku).first()
        if not db_product:
            return None
        return Product(
            id=db_product.id,
            name=db_product.name,
            sku=db_product.sku,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    def create(self, product: Product) -> Product:
        db_product = models.Product(
            name=product.name,
            sku=product.sku,
            price=product.price,
            quantity=product.quantity,
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return Product(
            id=db_product.id,
            name=db_product.name,
            sku=db_product.sku,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    def update(self, product: Product) -> Product:
        db_product = self.db.query(models.Product).filter(models.Product.id == product.id).first()
        if not db_product:
            return None

        db_product.name = product.name
        db_product.sku = product.sku
        db_product.price = product.price
        db_product.quantity = product.quantity

        self.db.commit()
        self.db.refresh(db_product)
        return Product(
            id=db_product.id,
            name=db_product.name,
            sku=db_product.sku,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    def delete(self, product_id: int) -> bool:
        db_product = self.db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return False
        self.db.delete(db_product)
        self.db.commit()
        return True

    def exists_by_sku(self, sku: str, exclude_id: Optional[int] = None) -> bool:
        query = self.db.query(models.Product).filter(models.Product.sku == sku)
        if exclude_id:
            query = query.filter(models.Product.id != exclude_id)
        return query.first() is not None


class SQLAlchemyCustomerRepository(ICustomerRepository):
    """SQLAlchemy implementation of customer repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Customer]:
        db_customers = self.db.query(models.Customer).all()
        return [
            Customer(
                id=c.id,
                full_name=c.full_name,
                email=c.email,
                phone=c.phone,
            )
            for c in db_customers
        ]

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        db_customer = self.db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not db_customer:
            return None
        return Customer(
            id=db_customer.id,
            full_name=db_customer.full_name,
            email=db_customer.email,
            phone=db_customer.phone,
        )

    def get_by_email(self, email: str) -> Optional[Customer]:
        db_customer = self.db.query(models.Customer).filter(models.Customer.email == email).first()
        if not db_customer:
            return None
        return Customer(
            id=db_customer.id,
            full_name=db_customer.full_name,
            email=db_customer.email,
            phone=db_customer.phone,
        )

    def create(self, customer: Customer) -> Customer:
        db_customer = models.Customer(
            full_name=customer.full_name,
            email=customer.email,
            phone=customer.phone,
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return Customer(
            id=db_customer.id,
            full_name=db_customer.full_name,
            email=db_customer.email,
            phone=db_customer.phone,
        )

    def update(self, customer: Customer) -> Customer:
        db_customer = self.db.query(models.Customer).filter(models.Customer.id == customer.id).first()
        if not db_customer:
            return None

        db_customer.full_name = customer.full_name
        db_customer.email = customer.email
        db_customer.phone = customer.phone

        self.db.commit()
        self.db.refresh(db_customer)
        return Customer(
            id=db_customer.id,
            full_name=db_customer.full_name,
            email=db_customer.email,
            phone=db_customer.phone,
        )

    def delete(self, customer_id: int) -> bool:
        db_customer = self.db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not db_customer:
            return False
        self.db.delete(db_customer)
        self.db.commit()
        return True

    def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        query = self.db.query(models.Customer).filter(models.Customer.email == email)
        if exclude_id:
            query = query.filter(models.Customer.id != exclude_id)
        return query.first() is not None


class SQLAlchemyOrderRepository(IOrderRepository):
    """SQLAlchemy implementation of order repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Order]:
        db_orders = self.db.query(models.Order).all()
        return [
            Order(
                id=o.id,
                customer_id=o.customer_id,
                product_id=o.product_id,
                quantity=o.quantity,
                total_amount=o.total_amount,
                created_at=o.created_at,
            )
            for o in db_orders
        ]

    def get_by_id(self, order_id: int) -> Optional[Order]:
        db_order = self.db.query(models.Order).filter(models.Order.id == order_id).first()
        if not db_order:
            return None
        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            product_id=db_order.product_id,
            quantity=db_order.quantity,
            total_amount=db_order.total_amount,
            created_at=db_order.created_at,
        )

    def create(self, order: Order) -> Order:
        db_order = models.Order(
            customer_id=order.customer_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_amount=order.total_amount,
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            product_id=db_order.product_id,
            quantity=db_order.quantity,
            total_amount=db_order.total_amount,
            created_at=db_order.created_at,
        )

    def delete(self, order_id: int) -> bool:
        db_order = self.db.query(models.Order).filter(models.Order.id == order_id).first()
        if not db_order:
            return False
        self.db.delete(db_order)
        self.db.commit()
        return True
