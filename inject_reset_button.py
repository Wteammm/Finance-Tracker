import re

# Read the balance sheet template
template_path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Read the reset modal HTML
modal_path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\reset_modal.html'
with open(modal_path, 'r', encoding='utf-8') as f:
    modal_html = f.read()

# Find the location right before the closing </div> of the main container (before custom context menu)
# Add the hidden button and modal right before the closing container div
marker = '\u003c!-- Custom Context Menu --\u003e'

hidden_button_and_modal = '''
    \u003c!-- Hidden Admin Reset Button (Triple-click "Net Worth" to reveal) --\u003e
    \u003cdiv class=\"text-center mt-5 mb-3\"\u003e
        \u003csmall class=\"text-muted\" id=\"netWorthLabel\" style=\"cursor: pointer;\" title=\"Triple-click to reveal admin options\"\u003ePowered by Finance Tracker\u003c/small\u003e
        \u003cdiv id=\"adminPanel\" style=\"display: none;\" class=\"mt-2\"\u003e
            \u003cbutton type=\"button\" class=\"btn btn-sm btn-outline-danger\" data-bs-toggle=\"modal\" data-bs-target=\"#resetDataModal\"\u003e
                \u003ci class=\"bi bi-exclamation-triangle\"\u003e\u003c/i\u003e Reset All Data
            \u003c/button\u003e
        \u003c/div\u003e
    \u003c/div\u003e
\u003c/div\u003e

''' + modal_html + '''

\u003cscript\u003e
// Triple-click to reveal admin panel
let clickCount = 0;
let clickTimer;
document.getElementById('netWorthLabel').addEventListener('click', function() {
    clickCount++;
    clearTimeout(clickTimer);
    clickTimer = setTimeout(() => { clickCount = 0; }, 500);
    
    if (clickCount === 3) {
        const panel = document.getElementById('adminPanel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        clickCount = 0;
    }
});
\u003c/script\u003e

\u003c!-- Custom Context Menu --\u003e'''

# Replace the marker
if marker in content:
    content = content.replace(marker, hidden_button_and_modal, 1)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added hidden reset button and modal to balance_sheet.html")
else:
    print("ERROR: Marker not found")
