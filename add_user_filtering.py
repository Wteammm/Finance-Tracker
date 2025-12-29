"""
Script to add user_id filtering to all routes in app.py for data isolation.
This will update queries and new record creation to use session['user_id'].
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix index route - add user_id when creating new transaction
content = content.replace(
    "        new_transaction = Transaction(date=date_obj, category=category, description=description, amount=amount, account_id=account_id)\n        db.session.add(new_transaction)",
    "        new_transaction = Transaction(date=date_obj, category=category, description=description, amount=amount, account_id=account_id, user_id=session.get('user_id'))\n        db.session.add(new_transaction)"
)

# 2. Fix index route - filter transactions by user_id when querying
content = content.replace(
    "    transactions = Transaction.query.order_by(Transaction.date.desc()).all()",
    "    transactions = Transaction.query.filter_by(user_id=session.get('user_id')).order_by(Transaction.date.desc()).all()"
)

# 3. Fix balance calculation - filter by user_id
content = content.replace(
    "    total_balance = db.session.query(func.sum(Transaction.amount)).scalar() or 0",
    "    total_balance = db.session.query(func.sum(Transaction.amount)).filter(Transaction.user_id == session.get('user_id')).scalar() or 0"
)

# 4. Fix delete transaction route - ensure user owns the transaction
content = content.replace(
    "@app.route('/delete/<int:id>')\n@login_required\ndef delete_transaction(id):\n    transaction = Transaction.query.get_or_404(id)\n    db.session.delete(transaction)",
    "@app.route('/delete/<int:id>')\n@login_required\ndef delete_transaction(id):\n    transaction = Transaction.query.filter_by(id=id, user_id=session.get('user_id')).first_or_404()\n    db.session.delete(transaction)"
)

# 5. Fix balance sheet routes - filter BalanceItem by user_id
content = content.replace(
    "    items = BalanceItem.query.all()",
    "    items = BalanceItem.query.filter_by(user_id=session.get('user_id')).all()"
)

# 6. Fix add balance item - set user_id
content = content.replace(
    "        new_item = BalanceItem(\n            classification=classification,\n            name=name,\n            value=value,\n            liquidity_tier=liquidity_tier,\n            asset_type=asset_type,\n            obligation_type=obligation_type\n        )",
    "        new_item = BalanceItem(\n            classification=classification,\n            name=name,\n            value=value,\n            liquidity_tier=liquidity_tier,\n            asset_type=asset_type,\n            obligation_type=obligation_type,\n            user_id=session.get('user_id')\n        )"
)

# 7. Fix update balance item - ensure user owns it
content = content.replace(
    "    item = BalanceItem.query.get_or_404(item_id)",
    "    item = BalanceItem.query.filter_by(id=item_id, user_id=session.get('user_id')).first_or_404()"
)

# 8. Fix delete balance item - ensure user owns it
content = content.replace(
    "@app.route('/balance_sheet/delete/<int:item_id>', methods=['POST'])\n@login_required\ndef delete_balance_item(item_id):\n    item = BalanceItem.query.get_or_404(item_id)",
    "@app.route('/balance_sheet/delete/<int:item_id>', methods=['POST'])\n@login_required\ndef delete_balance_item(item_id):\n    item = BalanceItem.query.filter_by(id=item_id, user_id=session.get('user_id')).first_or_404()"
)

# 9. Fix investment routes - filter by user_id
content = content.replace(
    "    investments = Investment.query.order_by(Investment.date.desc()).all()",
    "    investments = Investment.query.filter_by(user_id=session.get('user_id')).order_by(Investment.date.desc()).all()"
)

# 10. Fix add investment - set user_id
content = content.replace(
    "        new_investment = Investment(\n            date=date_obj,\n            type=inv_type,\n            symbol=symbol,\n            market=market,\n            quantity=quantity,\n            price=price,\n            fees=fees,\n            currency=currency,\n            exchange_rate=exchange_rate,\n            remark=remark,\n            brokerage=brokerage\n        )",
    "        new_investment = Investment(\n            date=date_obj,\n            type=inv_type,\n            symbol=symbol,\n            market=market,\n            quantity=quantity,\n            price=price,\n            fees=fees,\n            currency=currency,\n            exchange_rate=exchange_rate,\n            remark=remark,\n            brokerage=brokerage,\n            user_id=session.get('user_id')\n        )"
)

# 11. Fix delete investment - ensure user owns it
content = content.replace(
    "@app.route('/portfolio/delete/<int:id>', methods=['POST'])\n@login_required\ndef delete_investment(id):\n    investment = Investment.query.get_or_404(id)",
    "@app.route('/portfolio/delete/<int:id>', methods=['POST'])\n@login_required\ndef delete_investment(id):\n    investment = Investment.query.filter_by(id=id, user_id=session.get('user_id')).first_or_404()"
)

# 12. Fix balance history - filter by user_id
content = content.replace(
    "    history = BalanceHistory.query.filter_by(item_id=item_id).order_by(BalanceHistory.date.desc()).all()",
    "    history = BalanceHistory.query.filter_by(item_id=item_id, user_id=session.get('user_id')).order_by(BalanceHistory.date.desc()).all()"
)

# 13. Fix add balance history - set user_id
content = content.replace(
    "        history_entry = BalanceHistory(\n            item_id=item.id,\n            old_value=old_value,\n            new_value=new_value,\n            adjustment=adjustment,\n            contra_account_id=contra_account_id,\n            contra_account_name=contra_account_name,\n            description=description\n        )",
    "        history_entry = BalanceHistory(\n            item_id=item.id,\n            old_value=old_value,\n            new_value=new_value,\n            adjustment=adjustment,\n            contra_account_id=contra_account_id,\n            contra_account_name=contra_account_name,\n            description=description,\n            user_id=session.get('user_id')\n        )"
)

# Write the updated content
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated app.py with user_id filtering in all routes")
print(f"File size: {len(content)} bytes")
print(f"Line count: {len(content.splitlines())}")
