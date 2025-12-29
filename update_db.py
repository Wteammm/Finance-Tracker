from app import app, db
import sys

try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)
