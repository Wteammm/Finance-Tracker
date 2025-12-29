from app import app, db, BalanceItem, Transaction

def force_delete():
    with app.app_context():
        items_to_delete = ['MBB', 'CIMB', 'PBB']
        for name in items_to_delete:
            item = BalanceItem.query.filter_by(name=name).first()
            if item:
                print(f"Found {name} (ID: {item.id})")
                # Unlink transactions
                txns = Transaction.query.filter_by(account_id=item.id).all()
                if txns:
                    print(f"  Unlinking {len(txns)} transactions...")
                    for t in txns:
                        t.account_id = None
                
                db.session.delete(item)
                print(f"  Deleted {name}.")
            else:
                print(f"Could not find {name}.")
        
        try:
            db.session.commit()
            print("Changes committed to database.")
        except Exception as e:
            print(f"Error committing changes: {e}")
            db.session.rollback()

if __name__ == '__main__':
    force_delete()
