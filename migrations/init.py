from app.models import init_db
import sys

if __name__ == '__main__':
    try:
        print("Initializing database...")
        init_db()
        print("✓ Database initialized successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        sys.exit(1)
