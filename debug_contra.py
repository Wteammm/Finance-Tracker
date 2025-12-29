from app import app, db, BalanceItem
try:
    app.app_context().push()
    
    mbb = BalanceItem.query.filter_by(name='MBB').first()
    loura = BalanceItem.query.filter_by(name='Loura').first()
    
    if not mbb or not loura:
        print(f"Items not found: MBB={mbb}, Loura={loura}")
        exit()

    print(f"MBB: Class='{mbb.classification}', Value={mbb.value}")
    print(f"Loura: Class='{loura.classification}', Value={loura.value}")
    
    def is_asset(c):
        return 'Asset' in c
    
    asset_m = is_asset(mbb.classification)
    asset_l = is_asset(loura.classification)
    print(f"Is Asset MBB: {asset_m}")
    print(f"Is Asset Loura: {asset_l}")
    
    # Simulate Logic: MBB (Asset) decreases by 500
    # Old = 1500 (Hypothetical start)
    # New = 1000
    diff = -500.0
    
    print(f"Simulating Diff: {diff}")
    
    if asset_m == asset_l:
        print("Asset == Asset. Condition TRUE.")
        print("Action: contra_item.value -= diff")
        expected_loura = loura.value - diff
        print(f"Current Loura ({loura.value}) - ({diff}) = {expected_loura}")
        # Assuming Loura started at 0
        print(f"If Loura started at 0: 0 - ({diff}) = {0 - diff}")
    else:
        print("Mismatch. Condition FALSE.")
        print("Action: contra_item.value += diff")
        print(f"Current Loura ({loura.value}) + ({diff}) = {loura.value + diff}")

except Exception as e:
    print(e)
