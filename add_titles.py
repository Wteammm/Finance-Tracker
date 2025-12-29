# Update all templates with dashboard titles

dashboard_titles = {
    'index.html': 'Daily Transaction',
    'chart.html': 'Transaction Overview',
    'portfolio.html': 'Investment',
    'portfolio_overview.html': 'Portfolio Overview',
    'add_investment.html': 'Add Investment',
    'cash_flow.html': 'Cash Flow',
    'balance_sheet.html': 'Net Worth'
}

for template, title in dashboard_titles.items():
    file_path = f'templates/{template}'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has dashboard_title block
        if '{% block dashboard_title %}' in content:
            print(f"Skipping {template} - already has title")
            continue
        
        # Find the dashboard block and add title block after it
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if '{% block dashboard %}' in line:
                # Add title block right after dashboard block
                new_lines.append(f'{{% block dashboard_title %}}{title}{{% endblock %}}')
        
        new_content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated {template} with title: {title}")
    except Exception as e:
        print(f"✗ Error with {template}: {e}")

print("\nAll templates updated with dashboard titles!")
