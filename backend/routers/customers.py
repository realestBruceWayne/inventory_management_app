from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.customer_service import CustomerService
from dependencies import get_customer_service
from domain.entities import Customer
from domain.exceptions import CustomerNotFoundException, CustomerEmailAlreadyExistsException
from rate_limit import limiter
from auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=list[schemas.Customer])
@limiter.limit("100/minute")
def read_customers(request: Request, customer_service: CustomerService = Depends(get_customer_service)):
    customers = customer_service.get_all_customers()
    return [schemas.Customer(**c.__dict__) for c in customers]

@router.get("/{customer_id}", response_model=schemas.Customer)
@limiter.limit("100/minute")
def read_customer(request: Request, customer_id: int, customer_service: CustomerService = Depends(get_customer_service)):
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        return schemas.Customer(**customer.__dict__)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=schemas.Customer)
@limiter.limit("30/minute")
def create_customer(request: Request, customer: schemas.CustomerCreate, customer_service: CustomerService = Depends(get_customer_service), current_user: dict = Depends(get_current_user)):
    try:
        customer_entity = Customer(**customer.model_dump())
        created_customer = customer_service.create_customer(customer_entity)
        return schemas.Customer(**created_customer.__dict__)
    except CustomerEmailAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{customer_id}")
@limiter.limit("20/minute")
def delete_customer(request: Request, customer_id: int, customer_service: CustomerService = Depends(get_customer_service), current_user: dict = Depends(get_current_user)):
    try:
        customer_service.delete_customer(customer_id)
        return {"message": "Customer deleted successfully"}
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{customer_id}", response_model=schemas.Customer)
@limiter.limit("30/minute")
def update_customer(request: Request, customer_id: int, customer: schemas.CustomerCreate, customer_service: CustomerService = Depends(get_customer_service), current_user: dict = Depends(get_current_user)):
    try:
        customer_entity = Customer(**customer.model_dump())
        updated_customer = customer_service.update_customer(customer_id, customer_entity)
        return schemas.Customer(**updated_customer.__dict__)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CustomerEmailAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
