from app import app, db, Transaction, Investment

with app.app_context():
    # Check for Dashboard transactions
    txs = Transaction.query.filter(Transaction.description.like('%Fetch%')).all()
    print(f"Found {len(txs)} transactions matching 'Fetch':")
    for tx in txs:
        print(f" - {tx.id}: {tx.description} ({tx.amount})")

    # Check for Portfolio investments
    invs = Investment.query.all()
    print(f"Found {len(invs)} investments.")
