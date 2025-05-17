import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Category, Product, Sale, Inventory


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_category():
    response = client.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data

def test_create_product():
    # First create a category
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    # Then create a product
    product_data = {
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert data["category_id"] == category_id

def test_create_sale():
    # First create necessary data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    # Create a sale
    sale_data = {
        "product_id": product_id,
        "quantity": 2,
        "total_price": 1999.98
    }
    response = client.post("/sales/", json=sale_data)
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["quantity"] == 2
    assert data["total_price"] == 1999.98

def test_create_inventory():
    # First create necessary data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    # Create inventory
    inventory_data = {
        "product_id": product_id,
        "stock_level": 10
    }
    response = client.post("/inventory/", json=inventory_data)
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["stock_level"] == 10

def test_get_products():
    # Create test data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })

    # Test get all products
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Laptop"

def test_get_sales():
    # Create test data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    client.post("/sales/", json={
        "product_id": product_id,
        "quantity": 2,
        "total_price": 1999.98
    })

    # Test get all sales
    response = client.get("/sales/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["product_id"] == product_id

def test_get_inventory():
    # Create test data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    client.post("/inventory/", json={
        "product_id": product_id,
        "stock_level": 10
    })

    # Test get all inventory
    response = client.get("/inventory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["product_id"] == product_id

def test_update_product():
    # Create test data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    # Update product
    update_data = {
        "name": "Updated Laptop",
        "price": 899.99
    }
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Laptop"
    assert data["price"] == 899.99

def test_delete_product():
    # Create test data
    category_response = client.post("/categories/", json={"name": "Electronics"})
    category_id = category_response.json()["id"]

    product_response = client.post("/products/", json={
        "name": "Laptop",
        "category_id": category_id,
        "price": 999.99
    })
    product_id = product_response.json()["id"]

    # Delete product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200

    # Verify product is deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404