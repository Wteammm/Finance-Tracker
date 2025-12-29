
path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'Powered by Finance Tracker'
index = content.find(target)
if index != -1:
    print(f"Found '{target}' at index {index}")
    # Print 500 chars before and 2000 chars after
    start = max(0, index - 500)
    end = min(len(content), index + 2000)
    print("--- CONTEXT ---")
    print(content[start:end])
    print("--- END CONTEXT ---")
else:
    print(f"'{target}' NOT FOUND in file")
