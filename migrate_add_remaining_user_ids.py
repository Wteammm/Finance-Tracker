"""
Database Migration Script: Add user_id to remaining models
This script adds user_id columns to ForexTransaction, PortfolioSnapshot, Mortgage, and MortgageEvent tables.
"""

from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Starting migration: Adding user_id columns to remaining models...")
        
        try:
            with db.engine.connect() as conn:
                # Add user_id to ForexTransaction
                try:
                    conn.execute(text("ALTER TABLE forex_transaction ADD COLUMN user_id INTEGER"))
                    conn.commit()
                    print("✓ Added user_id to forex_transaction")
                except Exception as e:
                    print(f"  forex_transaction.user_id already exists or error: {e}")
                
                # Add user_id to PortfolioSnapshot
                try:
                    conn.execute(text("ALTER TABLE portfolio_snapshot ADD COLUMN user_id INTEGER"))
                    conn.commit()
                    print("✓ Added user_id to portfolio_snapshot")
                except Exception as e:
                    print(f"  portfolio_snapshot.user_id already exists or error: {e}")
                
                # Add user_id to Mortgage
                try:
                    conn.execute(text("ALTER TABLE mortgage ADD COLUMN user_id INTEGER"))
                    conn.commit()
                    print("✓ Added user_id to mortgage")
                except Exception as e:
                    print(f"  mortgage.user_id already exists or error: {e}")
                
                # Add user_id to MortgageEvent
                try:
                    conn.execute(text("ALTER TABLE mortgage_event ADD COLUMN user_id INTEGER"))
                    conn.commit()
                    print("✓ Added user_id to mortgage_event")
                except Exception as e:
                    print(f"  mortgage_event.user_id already exists or error: {e}")
            
            print("\n✅ Migration completed successfully!")
            print("\nNext steps:")
            print("1. Run assign_existing_data.py to assign existing data to users")
            print("2. Test the application with multiple users")
            print("3. Deploy to PythonAnywhere")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            raise

if __name__ == '__main__':
    migrate()
