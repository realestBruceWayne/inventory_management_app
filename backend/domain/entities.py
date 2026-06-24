from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    sku: str = ""
    price: float = 0.0
    quantity: int = 0

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.price < 0:
            raise ValueError("Price cannot be negative")

    def decrease_quantity(self, amount: int) -> None:
        if amount > self.quantity:
            raise ValueError("Insufficient quantity")
        self.quantity -= amount

    def increase_quantity(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.quantity += amount

    def is_low_stock(self, threshold: int = 10) -> bool:
        return self.quantity <= threshold


@dataclass
class Customer:
    id: Optional[int] = None
    full_name: str = ""
    email: str = ""
    phone: Optional[str] = None

    def __post_init__(self):
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")


@dataclass
class Order:
    id: Optional[int] = None
    customer_id: int = 0
    product_id: int = 0
    quantity: int = 0
    total_amount: float = 0.0
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.total_amount < 0:
            raise ValueError("Total amount cannot be negative")

    def calculate_total(self, product_price: float) -> None:
        self.total_amount = product_price * self.quantity
