
path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the modal
idx = content.find('id="addItemModal"')
if idx != -1:
    print("Found modal at", idx)
    print(content[idx:idx+1500]) # Print enough to see the fields
else:
    print("Modal ID not found")
