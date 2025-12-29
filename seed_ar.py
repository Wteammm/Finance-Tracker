
from app import app, db, BalanceItem

def seed_ar():
    accounts = ["Loura", "Stella", "MM", "Others"]
    
    with app.app_context():
        for name in accounts:
            # Check if exists
            exists = BalanceItem.query.filter_by(name=name).first()
            if exists:
                # Update type if needed
                if exists.asset_type != 'AR':
                    exists.asset_type = 'AR'
                    exists.classification = 'Current Asset'
                    print(f"Updated {name} to AR type.")
                else:
                    print(f"Skipping {name}, already exists.")
            else:
                new_item = BalanceItem(
                    name=name,
                    classification='Current Asset',
                    asset_type='AR',
                    value=0.0,
                    liquidity_tier='None' # AR doesn't strictly need high/med/low, can be None or unclassified
                )
                db.session.add(new_item)
                print(f"Added {name}")
        
        db.session.commit()
        print("AR Seeding Complete.")

if __name__ == "__main__":
    seed_ar()
