# E-commerce Admin API

A FastAPI-based backend API for e-commerce management, providing detailed insights into sales, revenue, and inventory status.

## Features

### Sales Management
- Retrieve and filter sales data
- Analyze revenue (daily, weekly, monthly, annual)
- Compare revenue across periods and categories
- Get sales data by date range, product, and category

### Inventory Management
- View current inventory status
- Low stock alerts
- Update inventory levels
- Track inventory changes over time

## Technical Stack
- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## Setup Instructions

1. **Clone the repository**
```bash
git clone [your-repository-url]
cd ecommerce-admin-api
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the root directory:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
DB_USER=postgres
DB_PASS=your_password
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Populate demo data**
```bash
python data/seed_data.py
```

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Available Endpoints

#### Products
- `GET /products/` - List all products
- `POST /products/` - Create new product
- `GET /products/{id}` - Get product details
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

#### Sales
- `GET /sales/` - List all sales
- `POST /sales/` - Record new sale
- `GET /sales/revenue-analysis` - Get revenue analysis
- `GET /sales/filter` - Filter sales by date range

#### Inventory
- `GET /inventory/` - List all inventory items
- `POST /inventory/` - Add inventory item
- `GET /inventory/low-stock` - Get low stock alerts
- `PUT /inventory/{id}` - Update inventory level

## Database Schema

### Tables

#### Categories
- `id` (Primary Key)
- `name` (String)

#### Products
- `id` (Primary Key)
- `name` (String)
- `category_id` (Foreign Key)
- `price` (Float)
- `created_at` (DateTime)

#### Sales
- `id` (Primary Key)
- `product_id` (Foreign Key)
- `quantity` (Integer)
- `total_price` (Float)
- `sale_date` (DateTime)

#### Inventory
- `id` (Primary Key)
- `product_id` (Foreign Key)
- `stock_level` (Integer)
- `updated_at` (DateTime)

## Testing
Run the test suite:
```bash
pytest tests/test_api.py -v
```

## API Documentation
Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"# Backend-Development" 
