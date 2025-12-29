"""
Script to safely update app.py with user authentication changes.
This avoids file corruption issues by reading, modifying, and writing the entire file at once.
"""

# Read the current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove hashlib import
content = content.replace('import hashlib\n', '')

# 2. Remove PASSWORD_HASH constant (lines 15-16)
content = content.replace("# Password protection - SHA256 hash of \"1234\"\nPASSWORD_HASH = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'\n\n", '')

# 3. Add user_id to Transaction model (after account_id line)
content = content.replace(
    "    account_id = db.Column(db.Integer, db.ForeignKey('balance_item.id'), nullable=True) # Link to Source Account\n\n    def __repr__(self):",
    "    account_id = db.Column(db.Integer, db.ForeignKey('balance_item.id'), nullable=True) # Link to Source Account\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # User ownership\n\n    def __repr__(self):"
)

# 4. Add user_id to BalanceHistory model
content = content.replace(
    "    description = db.Column(db.String(200), nullable=True)\n    \n    def __repr__(self):\n        return f'<BalanceHistory {self.id} - Item {self.item_id}>'",
    "    description = db.Column(db.String(200), nullable=True)\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # User ownership\n    \n    def __repr__(self):\n        return f'<BalanceHistory {self.id} - Item {self.item_id}>'"
)

# 5. Add user_id to Investment model
content = content.replace(
    "    brokerage = db.Column(db.String(100), nullable=True) # Brokerage account (e.g., Moomoo, Maybank Trade)\n\n    def __repr__(self):\n        return f'<Investment {self.symbol} - {self.type}>'",
    "    brokerage = db.Column(db.String(100), nullable=True) # Brokerage account (e.g., Moomoo, Maybank Trade)\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # User ownership\n\n    def __repr__(self):\n        return f'<Investment {self.symbol} - {self.type}>'"
)

# 6. Add user_id to BalanceItem model
content = content.replace(
    "    auto_reminder_enabled = db.Column(db.Boolean, default=False)  # Toggle auto reminders per contact\n\n\nclass Mortgage(db.Model):",
    "    auto_reminder_enabled = db.Column(db.Boolean, default=False)  # Toggle auto reminders per contact\n    \n    # User ownership\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)\n\n\nclass Mortgage(db.Model):"
)

# 7. Update login_required decorator
content = content.replace(
    "        if not session.get('logged_in'):\n            return redirect(url_for('login'))",
    "        if not session.get('user_id'):\n            return redirect(url_for('login'))"
)

# 8. Update login route
old_login = """@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == PASSWORD_HASH:
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid password. Please try again.', 'danger')
    
    return render_template('login.html')"""

new_login = """@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')"""

content = content.replace(old_login, new_login)

# 9. Update logout route
old_logout = """@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))"""

new_logout = """@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))"""

content = content.replace(old_logout, new_logout)

# Write the updated content back to app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated app.py with user authentication changes")
print(f"File size: {len(content)} bytes")
print(f"Line count: {len(content.splitlines())}")
