from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Add liquidity_tier column
                conn.execute(text('ALTER TABLE balance_item ADD COLUMN liquidity_tier VARCHAR(20)'))
                conn.commit()
            print("Migration successful: Added liquidity_tier column.")
        except Exception as e:
            print(f"Migration failed (maybe column exists?): {e}")

if __name__ == "__main__":
    migrate()
