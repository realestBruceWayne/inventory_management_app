# Inventory & Order Management System

A full-stack inventory and order management system with a FastAPI backend and React frontend.

## Features

- **Product Management**: Create, read, update, and delete products
- **Customer Management**: Manage customer information
- **Order Processing**: Create and manage orders with inventory validation
- **Dashboard**: Overview of system status and low stock alerts
- **Authentication**: JWT-based authentication for protected endpoints
- **Rate Limiting**: API rate limiting to prevent abuse

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- PostgreSQL - Database
- JWT - Authentication
- SlowAPI - Rate limiting

### Frontend
- React - UI framework
- Axios - HTTP client

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Authentication

The system uses JWT authentication. To obtain a token:

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Use the returned token in the Authorization header for protected endpoints:
```
Authorization: Bearer <your_token>
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- Default endpoints: 100 requests/minute
- Write operations: 30 requests/minute
- Delete operations: 20 requests/minute
- Authentication: 10 requests/minute

## Deployment

### Backend
The backend can be deployed to:
- Render
- Railway
- Fly.io

### Frontend
The frontend can be deployed to:
- Vercel
- Netlify

## License

MIT