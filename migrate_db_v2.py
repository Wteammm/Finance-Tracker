from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # 'transaction' is a reserved word, must be quoted
                conn.execute(text('ALTER TABLE "transaction" ADD COLUMN account_id INTEGER'))
                conn.commit()
            print("Migration successful: Added account_id column.")
        except Exception as e:
            print(f"Migration failed (maybe column exists?): {e}")

if __name__ == "__main__":
    migrate()
