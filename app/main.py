from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import sales, inventory, products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

# Include routers
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(sales.router, prefix="/api/v1", tags=["sales"])
app.include_router(inventory.router, prefix="/api/v1", tags=["inventory"])

@app.get("/")
def root():
    return {"message": "Welcome to E-commerce Admin API"}
