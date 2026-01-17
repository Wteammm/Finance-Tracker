from app import app, db, User, Transaction, BalanceItem
import os

with app.app_context():
    print("="*50)
    print("FINANCE TRACKER - DATA DIAGNOSTIC")
    print("="*50)
    
    # Check Database File
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_uri.replace('sqlite:///', '')
    print(f"\n1. Database Path: {db_path}")
    if os.path.exists(db_path):
        size = os.path.getsize(db_path) / 1024
        print(f"   Status: FOUND")
        print(f"   Size: {size:.2f} KB")
    else:
        print(f"   Status: NOT FOUND")
        print("="*50)
        exit()

    # Check Users
    print("\n2. Users found in database:")
    users = User.query.all()
    if not users:
        print("   Status: NO USERS FOUND")
    else:
        for u in users:
            tx_count = Transaction.query.filter_by(user_id=u.id).count()
            print(f"   - User ID: {u.id}, Username: '{u.username}', Transactions: {tx_count}")

    # Check Total Transactions
    total_tx = Transaction.query.count()
    print(f"\n3. Total Transactions (all users): {total_tx}")

    # Check Linked Accounts
    accounts = BalanceItem.query.all()
    print(f"\n4. Linked Accounts found: {len(accounts)}")
    for acc in accounts:
        print(f"   - Account: {acc.name}, User ID: {acc.user_id}")

    print("\n" + "="*50)
    print("DIAGNOSIS COMPLETE")
    print("="*50)
