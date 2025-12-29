# Quick script to create User table in database
from app import app, db, User

with app.app_context():
    # Create User table
    db.create_all()
    print("User table created successfully!")
