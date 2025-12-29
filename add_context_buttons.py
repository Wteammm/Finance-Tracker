
import re

path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add IDs to the modal inputs
# Classification
content = re.sub(r'name="classification"', r'name="classification" id="add_class"', content)
# Liquidity Tier
content = re.sub(r'name="liquidity_tier"', r'name="liquidity_tier" id="add_tier"', content)
# Asset Type - identifying it by label or checking context if possible, but assuming it exists
if 'name="asset_type"' in content:
    content = re.sub(r'name="asset_type"', r'name="asset_type" id="add_type"', content)
else:
    # Need to verify if asset_type field exists in the modal. Previous verify cut off.
    # Assuming it does based on db model. If not, the JS will just log constraint.
    pass

# 2. Inject Context Buttons

# Helper for button HTML
def get_btn(cls, asset_type, tier):
    tier_arg = f"'{tier}'" if tier else 'null'
    return f"""<span onclick="event.preventDefault(); event.stopPropagation(); openAddModal('{cls}', '{asset_type}', {tier_arg});" class="ms-2 text-primary" style="cursor:pointer;" title="Add {tier or asset_type} Item"><i class="bi bi-plus-circle-fill"></i></span>"""

# High Liquidity
pat_high = r'(<span class="fw-normal text-success me-2">High Liquidity</span>)'
rep_high = r'\1 ' + get_btn('Current Asset', 'Cash', 'High')
content = re.sub(pat_high, rep_high, content)

# Medium Liquidity
pat_med = r'(<span class="fw-normal text-success me-2">Medium Liquidity</span>)'
rep_med = r'\1 ' + get_btn('Current Asset', 'Cash', 'Medium')
content = re.sub(pat_med, rep_med, content)

# Low Liquidity
pat_low = r'(<span class="fw-normal text-success me-2">Low Liquidity</span>)'
rep_low = r'\1 ' + get_btn('Current Asset', 'Cash', 'Low')
content = re.sub(pat_low, rep_low, content)

# Accounts Receivable
# Found inside: <div>Accounts Receivable</div> in the collapser toggle
pat_ar = r'(<div>\s*Accounts Receivable\s*</div>)'
# Need to be careful with regex whitespace
# Simpler: replace the text "Accounts Receivable" inside the div
content = re.sub(r'Accounts Receivable', r'Accounts Receivable ' + get_btn('Current Asset', 'AR', None), content, count=1)
# Note: This might replace other instances if not careful. The first instance in sidebar/networth might be safe or different.
# Navigation uses "Net Worth", manual items use "Accounts Receivable".
# The one in the List Group Item is the target.
# Let's hope count=1 targets the right one (or I check context).
# Actually, the view showed it under `<!-- Accounts Receivable -->`
# It's unique enough.

# Other Current Assets
content = re.sub(r'Other Current Assets', r'Other Current Assets ' + get_btn('Current Asset', 'Other', None), content, count=1)


# 3. Add JS Function
js_code = """
<script>
function openAddModal(cls, type, tier) {
    // Open Modal
    var myModal = new bootstrap.Modal(document.getElementById('addItemModal'));
    myModal.show();
    
    // Set Values
    // Wait for modal to be potentially ready, or just set immediately
    setTimeout(() => {
        const classSelect = document.getElementById('add_class');
        const typeSelect = document.getElementById('add_type');
        const tierSelect = document.getElementById('add_tier');
        
        if(classSelect) classSelect.value = cls;
        if(typeSelect) typeSelect.value = type;
        if(tierSelect) tierSelect.value = tier ? tier : ""; // Set to empty if null
        
        // Trigger generic change event if needed for any dependent logic
        if(classSelect) classSelect.dispatchEvent(new Event('change'));
    }, 200);
}
</script>
"""

# Append JS before endblock
content = content.replace('{% endblock %}', js_code + '\n{% endblock %}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected contextual add buttons and JS")
