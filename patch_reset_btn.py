import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the broken event listener
# It starts with document.getElementById('resetForm').addEventListener('submit'
# And contains "confirm("
pattern = r"document\.getElementById\('resetForm'\)\.addEventListener\('submit', function\(e\) \{[\s\S]*?\}\);"

replacement = r"""
// Form submission - simple confirmation
document.getElementById('resetForm').addEventListener('submit', function(e) {
    // No extra confirm needed as typing is enough
    // Just let it submit
});
"""

if re.search(pattern, content):
    new_content = re.sub(pattern, replacement, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched reset form submission logic")
else:
    print("ERROR: Could not find reset form event listener to patch")
    # Print a snippet to help debug
    idx = content.find("resetForm")
    if idx != -1:
        print("Found resetForm at", idx)
        print(content[idx:idx+200])
