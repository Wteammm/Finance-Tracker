
from app import app, db, BalanceItem

with app.app_context():
    ar_items = BalanceItem.query.filter_by(asset_type='AR').all()
    print("Existing AR Accounts:")
    if not ar_items:
        print("None")
    else:
        for item in ar_items:
            print(f"- {item.name} (Value: {item.value})")
