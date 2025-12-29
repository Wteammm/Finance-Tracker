
path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Look for the comment
target = "// Form submission with final confirmation"
idx = content.find(target)

if idx != -1:
    print(f"Found target at {idx}")
    # Extract the block
    print(content[idx:idx+300])
    
    # We want to replace from this comment until the end of the script block or reasonable end
    # The block looks like:
    # // Form submission with final confirmation
    # document.getElementById('resetForm').addEventListener('submit', function(e) {
    #    e.preventDefault();
    #    if (confirm('FINAL WARNING: Are you absolutely sure you want to delete ALL data? This cannot be undone!')) {
    #        this.submit();
    #    }
    # });
    
    # Let's verify we can find the end
    end_marker = "});"
    end_idx = content.find(end_marker, idx)
    if end_idx != -1:
        full_block = content[idx:end_idx+3]
        print("\n--- FULL BLOCK TO REPLACE ---")
        print(full_block)
        
        replacement = """// Form submission - simplified
document.getElementById('resetForm').addEventListener('submit', function(e) {
    // Check if button is disabled (should be handled by browser but good to double check)
    if (document.getElementById('confirmResetBtn').disabled) {
        e.preventDefault();
        return false;
    }
    // Allow submission
    return true;
});"""
        
        new_content = content.replace(full_block, replacement)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("\nSUCCESS: Replaced code block")
    else:
        print("Could not find end of block")
else:
    print("Target comment not found")
