# API Documentation

## Overview
The E-commerce Admin API provides endpoints for managing products, sales, and inventory. All endpoints are prefixed with `/api/v1`.

## Authentication
Currently, the API does not require authentication. In a production environment, JWT authentication should be implemented.

## Endpoints

### Products

#### List Products
```http
GET /api/v1/products/
```
**Response**: List of all products
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "category_id": 1,
    "price": 999.99,
    "created_at": "2024-03-20T10:00:00"
  }
]
```

#### Create Product
```http
POST /api/v1/products/
```
**Request Body**:
```json
{
  "name": "Laptop",
  "category_id": 1,
  "price": 999.99
}
```
**Response**: Created product details

#### Get Product
```http
GET /api/v1/products/{id}
```
**Response**: Product details

#### Update Product
```http
PUT /api/v1/products/{id}
```
**Request Body**:
```json
{
  "name": "Updated Laptop",
  "price": 899.99
}
```
**Response**: Updated product details

#### Delete Product
```http
DELETE /api/v1/products/{id}
```
**Response**: Success message

### Sales

#### List Sales
```http
GET /api/v1/sales/
```
**Query Parameters**:
- `start_date`: Filter by start date
- `end_date`: Filter by end date
- `product_id`: Filter by product
- `category_id`: Filter by category

**Response**: List of sales

#### Create Sale
```http
POST /api/v1/sales/
```
**Request Body**:
```json
{
  "product_id": 1,
  "quantity": 2,
  "total_price": 1999.98
}
```
**Response**: Created sale details

#### Revenue Analysis
```http
GET /api/v1/sales/revenue-analysis
```
**Query Parameters**:
- `period`: daily/weekly/monthly/annual
- `start_date`: Start date for analysis
- `end_date`: End date for analysis

**Response**: Revenue analysis data

### Inventory

#### List Inventory
```http
GET /api/v1/inventory/
```
**Response**: List of all inventory items

#### Create Inventory Item
```http
POST /api/v1/inventory/
```
**Request Body**:
```json
{
  "product_id": 1,
  "stock_level": 100
}
```
**Response**: Created inventory item details

#### Update Inventory
```http
PUT /api/v1/inventory/{id}
```
**Request Body**:
```json
{
  "stock_level": 90
}
```
**Response**: Updated inventory details

#### Low Stock Alerts
```http
GET /api/v1/inventory/low-stock
```
**Query Parameters**:
- `threshold`: Minimum stock level (default: 10)

**Response**: List of products with low stock

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting
Currently, no rate limiting is implemented. In production, rate limiting should be added to prevent abuse.

## Best Practices
1. Always include proper error handling
2. Use appropriate HTTP methods
3. Return meaningful error messages
4. Validate input data
5. Use proper HTTP status codes