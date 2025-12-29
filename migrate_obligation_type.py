from app import app, db
from sqlalchemy import text

with app.app_context():
    # Add obligation_type column to balance_item table
    db.session.execute(text('ALTER TABLE balance_item ADD COLUMN obligation_type VARCHAR(30) DEFAULT "Standard"'))
    db.session.commit()
    print('Migration complete: Added obligation_type column')
