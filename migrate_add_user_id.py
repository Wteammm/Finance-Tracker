# Database Migration Script - Add user_id to all tables
# Run this ONCE after updating app.py

from app import app, db
from sqlalchemy import text

with app.app_context():
    # Add user_id columns to existing tables
    print("Starting database migration...")
    
    try:
        with db.engine.connect() as conn:
            # Add user_id to transaction table (use quotes because 'transaction' is reserved)
            try:
                conn.execute(text('ALTER TABLE "transaction" ADD COLUMN user_id INTEGER'))
                conn.commit()
                print("[OK] Added user_id to transaction table")
            except Exception as e:
                print(f"[SKIP] transaction.user_id: {str(e)[:50]}")
            
            # Add user_id to balance_item table
            try:
                conn.execute(text("ALTER TABLE balance_item ADD COLUMN user_id INTEGER"))
                conn.commit()
                print("[OK] Added user_id to balance_item table")
            except Exception as e:
                print(f"[SKIP] balance_item.user_id: {str(e)[:50]}")
            
            # Add user_id to balance_history table
            try:
                conn.execute(text("ALTER TABLE balance_history ADD COLUMN user_id INTEGER"))
                conn.commit()
                print("[OK] Added user_id to balance_history table")
            except Exception as e:
                print(f"[SKIP] balance_history.user_id: {str(e)[:50]}")
            
            # Add user_id to investment table
            try:
                conn.execute(text("ALTER TABLE investment ADD COLUMN user_id INTEGER"))
                conn.commit()
                print("[OK] Added user_id to investment table")
            except Exception as e:
                print(f"[SKIP] investment.user_id: {str(e)[:50]}")
            
            print("\n[SUCCESS] Migration completed!")
            print("\nNext steps:")
            print("1. Assign existing data to a user (run assign_existing_data.py)")
            print("2. Update routes to filter by user_id")
            print("3. Test with multiple users")
            
    except Exception as e:
        print(f"[ERROR] Migration failed: {str(e)}")
