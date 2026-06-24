from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.product_service import ProductService
from dependencies import get_product_service
from domain.entities import Product
from domain.exceptions import ProductNotFoundException, ProductSKUAlreadyExistsException
from rate_limit import limiter
from auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[schemas.Product])
@limiter.limit("100/minute")
def read_products(request: Request, product_service: ProductService = Depends(get_product_service)):
    products = product_service.get_all_products()
    return [schemas.Product(**p.__dict__) for p in products]

@router.get("/{product_id}", response_model=schemas.Product)
@limiter.limit("100/minute")
def read_product(request: Request, product_id: int, product_service: ProductService = Depends(get_product_service)):
    try:
        product = product_service.get_product_by_id(product_id)
        return schemas.Product(**product.__dict__)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=schemas.Product)
@limiter.limit("30/minute")
def create_product(request: Request, product: schemas.ProductCreate, product_service: ProductService = Depends(get_product_service), current_user: dict = Depends(get_current_user)):
    try:
        product_entity = Product(**product.model_dump())
        created_product = product_service.create_product(product_entity)
        return schemas.Product(**created_product.__dict__)
    except ProductSKUAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=schemas.Product)
@limiter.limit("30/minute")
def update_product(request: Request, product_id: int, product: schemas.ProductCreate, product_service: ProductService = Depends(get_product_service), current_user: dict = Depends(get_current_user)):
    try:
        product_entity = Product(**product.model_dump())
        updated_product = product_service.update_product(product_id, product_entity)
        return schemas.Product(**updated_product.__dict__)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductSKUAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
@limiter.limit("20/minute")
def delete_product(request: Request, product_id: int, product_service: ProductService = Depends(get_product_service), current_user: dict = Depends(get_current_user)):
    try:
        product_service.delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
