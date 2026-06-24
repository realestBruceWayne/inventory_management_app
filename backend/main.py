from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from database import engine, Base
from routers import products, customers, orders, dashboard
from rate_limit import limiter, rate_limit_error_handler, AUTH_RATE_LIMIT as auth_rate_limit
from auth import create_access_token, verify_password, get_password_hash
from pydantic import BaseModel
import os

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Order Management System",
    description="A full-stack inventory and order management system",
    version="1.0.0"
)

# Add rate limiter error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(dashboard.router)

# Simple login model
class LoginRequest(BaseModel):
    username: str
    password: str

# Simple user database (in production, use a real database)
USERS_DB = {
    "admin": {
        "username": "admin",
        "password_hash": get_password_hash("admin123")  # Change in production!
    }
}

@app.post("/token")
@limiter.limit(auth_rate_limit)
def login(request: Request, login_data: LoginRequest):
    """Simple authentication endpoint - returns JWT token"""
    user = USERS_DB.get(login_data.username)
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
@limiter.limit("50/minute")
def root(request: Request):
    return {
        "message": "Welcome to Inventory & Order Management System API",
        "docs": "/docs",
        "version": "1.0.0",
        "rate_limit": "50 requests per minute",
        "auth": "Use /token endpoint to get authentication token"
    }

@app.get("/health")
@limiter.limit("100/minute")
def health_check(request: Request):
    return {
        "status": "healthy",
        "database": "connected"
    }