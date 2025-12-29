#!/usr/bin/env python3
"""Fix: Add missing import modals to Balance Sheet and Portfolio"""

# Balance Sheet Modal
balance_modal = """
<!-- Import Modal -->
<div class="modal fade" id="importBalanceModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Import Balance Sheet from Excel</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="{{ url_for('import_balance_sheet') }}" enctype="multipart/form-data">
                <div class="modal-body">
                    <p>Upload an Excel file (.xlsx) with your balance sheet items.</p>
                    <div class="alert alert-info">
                        <strong>Format:</strong> Classification | Name | Value | Type | Liquidity Tier | Obligation Type<br>
                        <small>Classification: Current Asset/Non-Current Asset/Current Liability/Non-Current Liability. Duplicates will be skipped.</small>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Excel File</label>
                        <input type="file" class="form-control" name="file" accept=".xlsx" required>
                    </div>
                    <a href="{{ url_for('download_balance_sheet_template') }}" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-download"></i> Download Template
                    </a>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-success">Import</button>
                </div>
            </form>
        </div>
    </div>
</div>
"""

# Portfolio Modal
portfolio_modal = """
<!-- Import Modal -->
<div class="modal fade" id="importPortfolioModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Import Portfolio from Excel</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form method="POST" action="{{ url_for('import_portfolio') }}" enctype="multipart/form-data">
                <div class="modal-body">
                    <p>Upload an Excel file (.xlsx) with your investment data.</p>
                    <div class="alert alert-info">
                        <strong>Format:</strong> Date | Symbol | Type | Quantity | Price | Fees | Currency | Exchange Rate | Remark<br>
                        <small>Type: Buy/Sell/Dividend/Bonus/Split. Currency: MYR/USD. Duplicates will be skipped.</small>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Excel File</label>
                        <input type="file" class="form-control" name="file" accept=".xlsx" required>
                    </div>
                    <a href="{{ url_for('download_portfolio_template') }}" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-download"></i> Download Template
                    </a>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-success">Import</button>
                </div>
            </form>
        </div>
    </div>
</div>
"""

# Fix Balance Sheet
print("Checking Balance Sheet...")
with open('templates/balance_sheet.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'id="importBalanceModal"' not in content:
    # Insert before last {% endblock %}
    parts = content.rsplit('{% endblock %}', 1)
    new_content = parts[0] + balance_modal + '\n{% endblock %}' + (parts[1] if len(parts) > 1 else '')
    with open('templates/balance_sheet.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ Added Balance Sheet import modal")
else:
    print("✓ Balance Sheet modal already exists")

# Fix Portfolio
print("\nChecking Portfolio...")
with open('templates/portfolio.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'id="importPortfolioModal"' not in content:
    # Insert before last {% endblock %}
    parts = content.rsplit('{% endblock %}', 1)
    new_content = parts[0] + portfolio_modal + '\n{% endblock %}' + (parts[1] if len(parts) > 1 else '')
    with open('templates/portfolio.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ Added Portfolio import modal")
else:
    print("✓ Portfolio modal already exists")

print("\n✅ Done! Both import modals should now work.")
