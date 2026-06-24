from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from services.order_service import OrderService
from dependencies import get_order_service
from domain.entities import Order
from domain.exceptions import OrderNotFoundException, InsufficientInventoryException, ProductNotFoundException, CustomerNotFoundException
from rate_limit import limiter
from auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=list[schemas.Order])
@limiter.limit("100/minute")
def read_orders(request: Request, db: Session = Depends(get_db)):
    # Using direct database access for orders to include relationships
    orders = db.query(models.Order).all()
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
@limiter.limit("100/minute")
def read_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    # Using direct database access for orders to include relationships
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("", response_model=schemas.Order)
@limiter.limit("30/minute")
def create_order(request: Request, order: schemas.OrderCreate, order_service: OrderService = Depends(get_order_service), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        order_entity = Order(
            customer_id=order.customer_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_amount=0.0  # Will be calculated by service
        )
        created_order = order_service.create_order(order_entity)
        
        # Return the full order with relationships
        db_order = db.query(models.Order).filter(models.Order.id == created_order.id).first()
        return db_order
    except (InsufficientInventoryException, ProductNotFoundException, CustomerNotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_id}")
@limiter.limit("20/minute")
def delete_order(request: Request, order_id: int, order_service: OrderService = Depends(get_order_service), current_user: dict = Depends(get_current_user)):
    try:
        order_service.delete_order(order_id)
        return {"message": "Order deleted successfully"}
    except OrderNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
