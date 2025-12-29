from sqlalchemy import create_engine, Column, Integer, String, Float, text
import shutil
from datetime import datetime

# Backup database
db_path = 'instance/finance.db'
backup_name = f"instance/finance_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
shutil.copy(db_path, backup_name)
print(f"[OK] Backup created: {backup_name}")

# Connect to database
engine = create_engine('sqlite:///instance/finance.db')

# Add asset_type column
with engine.connect() as conn:
    try:
        # Add column (nullable for existing rows)
        conn.execute(text("ALTER TABLE balance_item ADD COLUMN asset_type VARCHAR"))
        conn.commit()
        print("[OK] Added asset_type column")
        
        # Set existing Current Assets to 'Cash'
        conn.execute(text("""
            UPDATE balance_item 
            SET asset_type = 'Cash'
            WHERE classification = 'Current Asset'
        """))
        conn.commit()
        print("[OK] Migrated existing Current Assets to 'Cash' type")
        
        # Verify
        result = conn.execute(text("""
            SELECT classification, asset_type, COUNT(*) 
            FROM balance_item 
            GROUP BY classification, asset_type
        """))
        
        print("\nMigration Summary:")
        for row in result:
            print(f"   {row[0]:<25} {row[1] or 'NULL':<15} Count: {row[2]}")
            
    except Exception as e:
        print(f"[ERROR] {e}")
        raise

print("\n[SUCCESS] Migration completed successfully!")

