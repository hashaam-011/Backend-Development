from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, Product, Sale, Inventory
import datetime

def seed_data():
    db = SessionLocal()
    try:
        # Create categories
        categories = [
            Category(name="Electronics"),
            Category(name="Clothing"),
            Category(name="Books")
        ]
        for category in categories:
            db.add(category)
        db.commit()

        # Create products
        products = [
            Product(name="Laptop", category_id=1, price=999.99),
            Product(name="T-shirt", category_id=2, price=19.99),
            Product(name="Novel", category_id=3, price=9.99)
        ]
        for product in products:
            db.add(product)
        db.commit()

        # Create sales
        sales = [
            Sale(product_id=1, quantity=2, total_price=1999.98),
            Sale(product_id=2, quantity=5, total_price=99.95),
            Sale(product_id=3, quantity=10, total_price=99.90)
        ]
        for sale in sales:
            db.add(sale)
        db.commit()

        # Create inventory
        inventory = [
            Inventory(product_id=1, stock_level=10),
            Inventory(product_id=2, stock_level=50),
            Inventory(product_id=3, stock_level=100)
        ]
        for item in inventory:
            db.add(item)
        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
    print("✅ Demo data seeded.")
