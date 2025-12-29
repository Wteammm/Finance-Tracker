# Simple update for dashboard titles

files = {
    'index.html': 'Daily Transaction',
    'chart.html': 'Transaction Overview',
    'portfolio.html': 'Investment',
    'portfolio_overview.html': 'Portfolio Overview',
    'add_investment.html': 'Add Investment',
    'cash_flow.html': 'Cash Flow',
    'balance_sheet.html': 'Net Worth'
}

for filename, title_text in files.items():
    path = f'templates/{filename}'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    
    new_lines = []
    for line in lines:
        new_lines.append(line)
        # Add title block after dashboard block
        if 'block dashboard' in line and 'endblock' in line:
            # Extract indentation
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}{{% block dashboard_title %}}{title_text}{{% endblock %}}")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"Updated {filename}")

print("Done!")
