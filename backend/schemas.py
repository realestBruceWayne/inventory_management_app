from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# Product Schemas
class ProductBase(BaseModel):
    name: str
    sku: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True

# Order Schemas
class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int = Field(gt=0)

class Order(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    created_at: Optional[datetime] = None
    
    product: Product
    customer: Customer

    class Config:
        from_attributes = True