# Database Documentation

## Overview
The E-commerce Admin API uses PostgreSQL as its database system. The database is designed to support all core functionalities including sales tracking, inventory management, and product management.

## Schema Design

### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```
**Purpose**: Stores product categories
**Relationships**: One-to-many with Products table

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Stores product information
**Relationships**:
- Many-to-one with Categories table
- One-to-many with Sales table
- One-to-one with Inventory table

### Sales Table
```sql
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Records sales transactions
**Relationships**: Many-to-one with Products table

### Inventory Table
```sql
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    stock_level INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Tracks product inventory levels
**Relationships**: One-to-one with Products table

## Indexes
```sql
-- Products table indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_created ON products(created_at);

-- Sales table indexes
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_sales_date ON sales(sale_date);

-- Inventory table indexes
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_stock ON inventory(stock_level);
```

## Data Integrity
- Foreign key constraints ensure referential integrity
- NOT NULL constraints on required fields
- Default timestamps for tracking creation/updates
- Decimal precision for monetary values

## Performance Considerations
1. Indexed foreign keys for faster joins
2. Indexed date fields for efficient date-based queries
3. Appropriate data types for optimal storage
4. Normalized schema to prevent data redundancy

## Demo Data
The database can be populated with demo data using the `data/seed_data.py` script. This script creates:
- Sample categories
- Sample products
- Sample sales records
- Initial inventory levels

## Backup and Recovery
Regular database backups are recommended. The database can be backed up using:
```bash
pg_dump -U postgres ecommerce > backup.sql
```

## Security Considerations
1. Database credentials stored in environment variables
2. Connection pooling for efficient resource usage
3. Prepared statements to prevent SQL injection
4. Regular security updates for PostgreSQL