
import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper for button HTML
def get_btn(cls, asset_type, tier):
    tier_arg = f"'{tier}'" if tier else 'null'
    # Added z-index and position relative just in case
    return f"""<span onclick="event.preventDefault(); event.stopPropagation(); openAddModal('{cls}', '{asset_type}', {tier_arg});" class="ms-2 text-primary position-relative" style="cursor:pointer; z-index: 10;" title="Add {tier or asset_type} Item"><i class="bi bi-plus-circle-fill"></i></span>"""

# 1. Fix Comments (Clean up the mess)
# Pattern: <!-- Title <span... -->
content = re.sub(r'<!-- Accounts Receivable <span.*?-->', '<!-- Accounts Receivable -->', content)
content = re.sub(r'<!-- Other Current Assets <span.*?-->', '<!-- Other Current Assets -->', content)

# 2. Inject into DIVs for AR and Other
# Target: <div>\nAccounts Receivable\n</div>
# We use DOTALL to match newlines if needed, but simple whitespace matching is safer
content = re.sub(r'<div>\s*Accounts Receivable\s*</div>', 
                 r'<div>Accounts Receivable ' + get_btn('Current Asset', 'AR', None) + r'</div>', 
                 content)

content = re.sub(r'<div>\s*Other Current Assets\s*</div>', 
                 r'<div>Other Current Assets ' + get_btn('Current Asset', 'Other', None) + r'</div>', 
                 content)

# 3. Liquidity Buttons - Replace existing ones (if any) or re-inject if clean
# If the previous script ran, they are there.
# Let's just REPLACE the specific span block with the new one (with z-index)
# Old pattern: <span onclick=... class="ms-2 text-primary" ...>
# New pattern: ... class="ms-2 text-primary position-relative" ...

# Pattern to find the existing span
span_pattern = r'<span onclick="event\.preventDefault\(\); event\.stopPropagation\(\); openAddModal\(.*?\);" class="ms-2 text-primary" style="cursor:pointer;" title="Add .*? Item"><i class="bi bi-plus-circle-fill"></i></span>'

# We can find all occurrences and replace them with the new version?
# Or clearer: Re-do the header replacements from scratch?
# Since we know exactly what they look like, search and replace is fine.

# Just verifying we fix visibility if that's the issue.
# Wait, if the previous injection succeeded, the HTML is:
# <span ...>High Liquidity</span> <span onclick...>...</span>
# I'll replacing it to ensure correct attributes.

# Let's search for the "old" button html (without z-index) and add z-index
old_btn_start = r'class="ms-2 text-primary"'
new_btn_start = r'class="ms-2 text-primary position-relative" style="z-index: 1050;"' 
# Using regex to update style as well?
# Actually, let's just use string replace for simplicity if the pattern is consistent.
# Current: class="ms-2 text-primary" style="cursor:pointer;"
# Target: class="ms-2 text-primary position-relative" style="cursor:pointer; z-index:100;"

content = content.replace('class="ms-2 text-primary" style="cursor:pointer;"', 'class="ms-2 text-primary position-relative" style="cursor:pointer; z-index: 100;"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully repaired comments and re-injected/updated buttons")
