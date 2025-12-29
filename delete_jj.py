from app import app, db, BalanceItem, Transaction

def delete_jj():
    with app.app_context():
        item = BalanceItem.query.filter_by(name='JJ').first()
        if item:
            print(f"Found JJ (ID: {item.id}). Deleting...")
            # Unlink transactions
            txns = Transaction.query.filter_by(account_id=item.id).all()
            for t in txns:
                t.account_id = None
            
            db.session.delete(item)
            db.session.commit()
            print("Deleted JJ.")
        else:
            print("JJ not found.")

if __name__ == '__main__':
    delete_jj()
