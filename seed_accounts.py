from app import app, db, BalanceItem

def seed():
    with app.app_context():
        # Define accounts and their tiers based on user request
        tier_mapping = {
            'High': ['MBB', 'PBB', 'TNG9791', 'CIMB', 'Ryt', 'GXB', 'Amb', 'Mae', 'HLB', 'Cash on Hand'],
            'Medium': ['BOC', 'Forex Cash on hand', 'Wise', 'KDI-Save', 'TNG-Save', 'CIMB Loan Cash Account', 'FSMOne', 'Webull', 'Moomoo-Cash', 'Moomoo-Fund'],
            'Low': ['TNG9327', 'PBB-FD', 'HLB-FD', 'Moomoo-Cash (USD)', 'Moomoo-Fund (USD)']
        }

        # 1. Update Existing Items with Tiers if they match name
        existing_items = BalanceItem.query.all()
        existing_names = {item.name.lower(): item for item in existing_items}

        for tier, names in tier_mapping.items():
            for name in names:
                # Check case-insensitive
                if name.lower() in existing_names:
                    item = existing_names[name.lower()]
                    item.liquidity_tier = tier
                    item.classification = 'Current Asset' # Ensure classification
                    print(f"Updated {item.name} to {tier}")
                else:
                    # Create new if not exists
                    new_item = BalanceItem(
                        name=name,
                        value=0.0,
                        classification='Current Asset',
                        liquidity_tier=tier,
                        is_auto_linked=False
                    )
                    db.session.add(new_item)
                    print(f"Created {name} in {tier}")

        db.session.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    seed()
