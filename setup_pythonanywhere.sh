#!/bin/bash
# Finance Tracker - PythonAnywhere Setup Script
# Run this script in PythonAnywhere Bash console after uploading files

echo "=========================================="
echo "Finance Tracker - Automated Setup"
echo "=========================================="
echo ""

# Step 1: Navigate to home directory
echo "[1/8] Navigating to home directory..."
cd ~

# Step 2: Backup old installation (if exists)
if [ -d "Finance_Tracker" ]; then
    echo "[2/8] Backing up old installation..."
    mv Finance_Tracker Finance_Tracker_backup_$(date +%Y%m%d_%H%M%S)
    echo "✓ Old files backed up"
else
    echo "[2/8] No existing installation found"
fi

# Step 3: Create directory structure
echo "[3/8] Creating directory structure..."
mkdir -p Finance_Tracker/static/css
mkdir -p Finance_Tracker/static/js
mkdir -p Finance_Tracker/static/icons
mkdir -p Finance_Tracker/templates

echo "✓ Directories created"
echo ""
echo "=========================================="
echo "PAUSE: Upload Your Files Now"
echo "=========================================="
echo ""
echo "Please upload these files via the Files tab:"
echo ""
echo "Root directory (Finance_Tracker/):"
echo "  - app.py"
echo "  - requirements.txt"
echo "  - migrate_add_custom_categories.py"
echo ""
echo "static/css/:"
echo "  - design-system.css"
echo ""
echo "static/js/:"
echo "  - offline-db.js"
echo "  - sync-manager.js"
echo "  - service-worker.js"
echo ""
echo "static/:"
echo "  - manifest.json"
echo ""
echo "static/icons/:"
echo "  - icon-192x192.png"
echo "  - icon-512x512.png"
echo ""
echo "templates/:"
echo "  - All your .html files"
echo ""
echo "After uploading, press ENTER to continue..."
read

# Step 4: Create virtual environment
echo "[4/8] Creating virtual environment..."
cd ~/Finance_Tracker
python3.10 -m venv venv
echo "✓ Virtual environment created"

# Step 5: Activate virtual environment and install dependencies
echo "[5/8] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Step 6: Initialize database
echo "[6/8] Initializing database..."
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✓ Database tables created")
EOF

# Step 7: Run migrations
echo "[7/8] Running migrations..."
python migrate_add_custom_categories.py
echo "✓ Migrations completed"

# Step 8: Final checks
echo "[8/8] Running final checks..."
if [ -f "app.py" ]; then
    echo "✓ app.py found"
else
    echo "✗ app.py NOT found - please upload it!"
fi

if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt found"
else
    echo "✗ requirements.txt NOT found - please upload it!"
fi

if [ -d "venv" ]; then
    echo "✓ Virtual environment created"
else
    echo "✗ Virtual environment failed"
fi

if [ -f "finance_tracker.db" ]; then
    echo "✓ Database initialized"
else
    echo "✗ Database not found"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to Web tab on PythonAnywhere"
echo "2. Click 'Reload' button"
echo "3. Visit your app URL to test"
echo ""
echo "Your Finance Tracker is ready! 🎉"
