from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer")
    product = relationship("Product")

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_order_quantity_positive'),
    )