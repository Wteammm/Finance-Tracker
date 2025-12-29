# Update remaining templates with dashboard blocks and top_nav

templates_to_update = {
    'chart.html': {
        'dashboard': 'daily-transaction',
        'top_nav': '<a href="{{ url_for(\'chart\') }}" class="active">Transaction Overview</a>'
    },
    'cash_flow.html': {
        'dashboard': 'cash-flow',
        'top_nav': ''  # Empty for now
    },
    'balance_sheet.html': {
        'dashboard': 'net-worth',
        'top_nav': ''  # Empty for now
    },
    'portfolio_overview.html': {
        'dashboard': 'investment',
        'top_nav': '''<a href="{{ url_for('forex') }}" class="{% if request.endpoint == 'forex' %}active{% endif %}">Forex Manager</a>
<a href="{{ url_for('add_investment') }}" class="{% if request.endpoint == 'add_investment' %}active{% endif %}">Add Investment</a>
<a href="{{ url_for('portfolio_overview') }}" class="active">Portfolio Overview</a>'''
    },
    'add_investment.html': {
        'dashboard': 'investment',
        'top_nav': '''<a href="{{ url_for('forex') }}" class="{% if request.endpoint == 'forex' %}active{% endif %}">Forex Manager</a>
<a href="{{ url_for('add_investment') }}" class="active">Add Investment</a>
<a href="{{ url_for('portfolio_overview') }}" class="{% if request.endpoint == 'portfolio_overview' %}active{% endif %}">Portfolio Overview</a>'''
    },
}

import os

for template_name, config in templates_to_update.items():
    file_path = f'templates/{template_name}'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it already has the blocks
        if '{% block dashboard %}' in content:
            print(f"Skipping {template_name} - already updated")
            continue
        
        # Find the extends line and add blocks after it
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if "{% extends 'base.html' %}" in line:
                new_lines.append('')
                new_lines.append(f"{{% block dashboard %}}{config['dashboard']}{{% endblock %}}")
                new_lines.append('')
                if config['top_nav']:
                    new_lines.append('{% block top_nav %}')
                    new_lines.append(config['top_nav'])
                    new_lines.append('{% endblock %}')
                    new_lines.append('')
        
        new_content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated {template_name}")
    else:
        print(f"File not found: {template_name}")

print("\nAll templates updated!")
