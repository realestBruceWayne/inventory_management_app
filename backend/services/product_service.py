from typing import List, Optional
from repositories.interfaces import IProductRepository
from domain.entities import Product
from domain.exceptions import (
    ProductNotFoundException,
    ProductSKUAlreadyExistsException,
)


class ProductService:
    """Service for product business logic following Single Responsibility Principle"""

    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        """Retrieve all products"""
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """Retrieve a product by ID"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with ID {product_id} not found")
        return product

    def create_product(self, product: Product) -> Product:
        """Create a new product"""
        if self.product_repository.exists_by_sku(product.sku):
            raise ProductSKUAlreadyExistsException(f"Product with SKU {product.sku} already exists")
        return self.product_repository.create(product)

    def update_product(self, product_id: int, product: Product) -> Product:
        """Update an existing product"""
        existing_product = self.product_repository.get_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundException(f"Product with ID {product_id} not found")

        if self.product_repository.exists_by_sku(product.sku, exclude_id=product_id):
            raise ProductSKUAlreadyExistsException(f"Product with SKU {product.sku} already exists")

        product.id = product_id
        return self.product_repository.update(product)

    def delete_product(self, product_id: int) -> None:
        """Delete a product"""
        if not self.product_repository.get_by_id(product_id):
            raise ProductNotFoundException(f"Product with ID {product_id} not found")
        self.product_repository.delete(product_id)

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        all_products = self.product_repository.get_all()
        return [p for p in all_products if p.is_low_stock(threshold)]
