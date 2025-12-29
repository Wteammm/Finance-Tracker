
import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject Debug Title
# Check if title block exists
if '{% block title %}' not in content:
    content = content.replace("{% extends 'base.html' %}", "{% extends 'base.html' %}\n{% block title %}Balance Sheet DEBUG{% endblock %}")
else:
    content = re.sub(r'{% block title %}.*?{% endblock %}', '{% block title %}Balance Sheet DEBUG{% endblock %}', content)

# 2. Simplify High Liquidity Button
# Target the entire header block including the absolute button I added previously
# My previous regex replacement created:
# <h2 class="accordion-header position-relative">...<button ... position-absolute ...>...</button></h2>
# I will replace it with a simple version:
# <h2 class="accordion-header">...High Liquidity <a href="#" onclick="...">[+]</a> ...</h2>

# Regex to find the whole H2 block for High Liquidity
# It starts with <h2 class="accordion-header... and contains "High Liquidity"
# and ends with </h2>
# I'll use a fairly broad match but careful about greedy.

# Let's just find the specific text "High Liquidity" inside the button and append the link directly there.
# And revert the H2 class to simple "accordion-header" (removing position-relative) to be safe.

# Clean up previous injection mess if possible:
# Replace <h2 class="accordion-header position-relative"> with <h2 class="accordion-header">
content = content.replace('class="accordion-header position-relative"', 'class="accordion-header"')

# Remove the absolute button I added
# <button class="btn btn-sm btn-link position-absolute ... </button>
# This regex is tricky.
# Let's just SEARCH for the string "High Liquidity" and the surrounding span/small tags.
# Current state likely:
# <span class="fw-normal text-success me-2">High Liquidity</span> <small...
# I want:
# <span class="fw-normal text-success me-2">High Liquidity <a href="#" onclick="event.stopPropagation(); openAddModal('Current Asset', 'Cash', 'High'); return false;" class="text-decoration-none fw-bold">[+]</a></span>

# First, remove any existing "Add" buttons/spans near High Liquidity
# I'll rely on the fact that I'm injecting into the label span.
# But wait, the previous code had the button separately. I need to DELETE that separate button.
# Use regex to remove the button block.
# Pattern: <button class="btn btn-sm btn-link position-absolute.*?</button>
content = re.sub(r'<button class="btn btn-sm btn-link position-absolute.*?</button>', '', content, flags=re.DOTALL)

# Now inject the simple link into the label
# Match: <span class="fw-normal text-success me-2">High Liquidity</span>
# Replace: <span class="fw-normal text-success me-2">High Liquidity <a href="#" style="z-index:9999; position:relative;" onclick="event.stopPropagation(); openAddModal('Current Asset', 'Cash', 'High'); return false;">[+]</a></span>
content = re.sub(r'(<span class="fw-normal text-success me-2">\s*High Liquidity\s*</span>)', 
                 r'\1 <span style="z-index:9999; position:relative;" onclick="event.stopPropagation(); openAddModal(\'Current Asset\', \'Cash\', \'High\');" class="text-primary fw-bold ms-2">[+]</span>', 
                 content)

# Do the same for Medium/Low to be consistent
content = re.sub(r'(<span class="fw-normal text-success me-2">\s*Medium Liquidity\s*</span>)', 
                 r'\1 <span style="z-index:9999; position:relative;" onclick="event.stopPropagation(); openAddModal(\'Current Asset\', \'Cash\', \'Medium\');" class="text-primary fw-bold ms-2">[+]</span>', 
                 content)

content = re.sub(r'(<span class="fw-normal text-success me-2">\s*Low Liquidity\s*</span>)', 
                 r'\1 <span style="z-index:9999; position:relative;" onclick="event.stopPropagation(); openAddModal(\'Current Asset\', \'Cash\', \'Low\');" class="text-primary fw-bold ms-2">[+]</span>', 
                 content)

# For AR and Other, they are already simple blocks, likely working?
# The user said "Still no".
# Let's check AR block.
# <div>Accounts Receivable</div>... <button ...>
# I'll replace it with inline:
# <div>Accounts Receivable <span ...>[+]</span></div>
# Remove the separate button if present.
content = re.sub(r'<button class="btn btn-sm btn-link p-0 text-decoration-none".*?</button>', '', content, flags=re.DOTALL)

# Inject inline
content = re.sub(r'<div>\s*Accounts Receivable\s*</div>', 
                 r'<div>Accounts Receivable <span style="z-index:9999; position:relative; cursor:pointer;" onclick="event.preventDefault(); event.stopPropagation(); openAddModal(\'Current Asset\', \'AR\', null);" class="text-primary fw-bold ms-2">[+]</span></div>', 
                 content)

content = re.sub(r'<div>\s*Other Current Assets\s*</div>', 
                 r'<div>Other Current Assets <span style="z-index:9999; position:relative; cursor:pointer;" onclick="event.preventDefault(); event.stopPropagation(); openAddModal(\'Current Asset\', \'Other\', null);" class="text-primary fw-bold ms-2">[+]</span></div>', 
                 content)


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected debug title and simplified buttons")
