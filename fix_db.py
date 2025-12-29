from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE investment ADD COLUMN remark VARCHAR(200)"))
            conn.commit()
        print("Successfully added remark column.")
    except Exception as e:
        print(f"Error (might already exist): {e}")
