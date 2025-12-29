# Add Portfolio modal
with open('templates/portfolio.html', 'r', encoding='utf-8') as f:
    content = f.read()

modal = '''
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
                        <small>Type: Buy/Sell/Dividend/Bonus/Split. Currency: MYR/USD.</small>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Excel File</label>
                        <input type="file" class="form-control" name="file" accept=".xlsx" required>
                    </div>
                    <a href="{{ url_for('download_portfolio_template') }}" class="btn btn-sm btn-outline-secondary">
                        Download Template
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
'''

parts = content.rsplit('{%' + ' endblock %}', 1)
new_content = parts[0] + modal + '\n{%' + ' endblock' + ' %}' + (parts[1] if len(parts) > 1 else '')

with open('templates/portfolio.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done Portfolio')
