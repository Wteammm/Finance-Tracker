
import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the stray absolute button if it still exists
# Search for <button ... position-absolute ... </button>
# Be careful not to delete other things.
# I will use a specific signature to be safe.
# It was likely: <button class="btn btn-sm btn-link position-absolute top-50 end-0 translate-middle-y me-5 z-3 p-0"
content = re.sub(r'<button class="btn btn-sm btn-link position-absolute.*?</button>', '', content, flags=re.DOTALL)

# 2. Convert [+] text to Icon
# Pattern: >[+]</span>
# Replacement: ><i class="bi bi-plus-circle-fill"></i></span>
content = content.replace('>[+]</span>', '><i class="bi bi-plus-circle-fill"></i></span>')

# 3. Clean up the Debug Title Block (revert to original extend)
if '{% block title %}Balance Sheet DEBUG{% endblock %}' in content:
    content = content.replace('{% block title %}Balance Sheet DEBUG{% endblock %}', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully finalized buttons and cleaned up")
