from app.database import engine
from app.models import Base
from sqlalchemy import text

def init_db():
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))

    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        connection.execute(text("""
            INSERT INTO categories (name)
            VALUES ('General')
        """))

    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()