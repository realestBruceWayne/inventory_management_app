from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Customer, Order
from rate_limit import limiter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
@limiter.limit("100/minute")
def get_summary(request: Request, db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()
    low_stock = db.query(Product).filter(Product.quantity < 10).all()
    
    return {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "low_stock_count": len(low_stock),
        "low_stock_items": low_stock
    }
