import sys
import os
import time
from database import SessionLocal, engine, Base
from models import Product, Customer, Order
import random

def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 10
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            from sqlalchemy import text
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            print("Database is ready!")
            return True
        except Exception as e:
            print(f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    print("Failed to connect to database after maximum retries")
    return False

def seed_database():
    """Create mock data for the database"""
    print("Seeding database with mock data...")
    
    # Wait for database to be ready
    if not wait_for_db():
        sys.exit(1)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Product).count() > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        # Mock Products
        products_data = [
            {"name": "Wireless Bluetooth Headphones", "sku": "WBH-001", "price": 79.99, "quantity": 150},
            {"name": "USB-C Charging Cable", "sku": "UCC-002", "price": 12.99, "quantity": 500},
            {"name": "Laptop Stand Aluminum", "sku": "LSA-003", "price": 45.50, "quantity": 75},
            {"name": "Mechanical Keyboard RGB", "sku": "MKR-004", "price": 129.99, "quantity": 60},
            {"name": "Wireless Mouse Ergonomic", "sku": "WME-005", "price": 34.99, "quantity": 200},
            {"name": "27-inch 4K Monitor", "sku": "M4K-006", "price": 349.99, "quantity": 30},
            {"name": "Webcam HD 1080p", "sku": "WHD-007", "price": 59.99, "quantity": 90},
            {"name": "External SSD 1TB", "sku": "ESS-008", "price": 119.99, "quantity": 45},
            {"name": "Smartphone Case Premium", "sku": "SCP-009", "price": 24.99, "quantity": 300},
            {"name": "Portable Power Bank 20000mAh", "sku": "PPB-010", "price": 39.99, "quantity": 120},
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        
        db.commit()
        print(f"Created {len(products)} products")
        
        # Mock Customers
        customers_data = [
            {"full_name": "Alice Johnson", "email": "alice.johnson@email.com", "phone": "+1-555-0101"},
            {"full_name": "Bob Smith", "email": "bob.smith@email.com", "phone": "+1-555-0102"},
            {"full_name": "Carol Davis", "email": "carol.davis@email.com", "phone": "+1-555-0103"},
            {"full_name": "David Wilson", "email": "david.wilson@email.com", "phone": "+1-555-0104"},
            {"full_name": "Emma Brown", "email": "emma.brown@email.com", "phone": "+1-555-0105"},
        ]
        
        customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        print(f"Created {len(customers)} customers")
        
        # Mock Orders
        for _ in range(15):
            customer = random.choice(customers)
            product = random.choice(products)
            quantity = random.randint(1, 5)
            
            if product.quantity >= quantity:
                total_amount = product.price * quantity
                product.quantity -= quantity
                
                order = Order(
                    customer_id=customer.id,
                    product_id=product.id,
                    quantity=quantity,
                    total_amount=total_amount
                )
                db.add(order)
        
        db.commit()
        
        order_count = db.query(Order).count()
        print(f"Created {order_count} orders")
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
