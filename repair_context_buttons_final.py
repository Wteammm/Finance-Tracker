
import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Backslashes in onclick
# Replace \' with '
content = content.replace(r"\'", "'")

# 2. Remove the lingering absolute button
# It spans multiple lines now (lines 177-182 in the view)
# Pattern: <button\s+class="btn btn-sm btn-link position-absolute.*?</button>
# Use re.DOTALL to match newlines
content = re.sub(r'<button\s+class="btn btn-sm btn-link position-absolute.*?</button>', '', content, flags=re.DOTALL)

# 3. Clean up empty lines left behind? 
# The regex removal might leave a blank line. Not critical but nice to have.
# content = re.sub(r'\n\s*\n', '\n', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully removed backslashes and deleted absolute buttons")
