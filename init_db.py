from app.database import engine
from app.models import Base
from sqlalchemy import text

def init_db():
    # Drop all existing tables with CASCADE
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create initial category
    with engine.begin() as connection:
        connection.execute(text("""
            INSERT INTO categories (name)
            VALUES ('General')
        """))

    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()