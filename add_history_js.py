import re

# Read the template file
template_path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section after transaction fetching, before contra dropdown population
# Insert after the transaction fetch catch block
pattern = r'(document\.getElementById\(\'txn_body\'\)\.innerHTML = \'<tr><td colspan="3" class="text-center text-danger">Error loading transactions</td></tr>\';\s*}\);)\s*(//\s*Populate Contra Dropdown)'

history_fetch_code = r'''\1

                // Fetch Balance Changes History
                console.log('Fetching balance history for ID:', currentId);
                fetch('/balance_sheet/history/' + currentId)
                    .then(response => response.json())
                    .then(data => {
                        const historyBody = document.getElementById('history_body');
                        historyBody.innerHTML = '';
                        if (data.length === 0) {
                            historyBody.innerHTML = '<tr><td colspan="5" class="text-center fst-italic">No balance changes recorded</td></tr>';
                        } else {
                            data.forEach(h => {
                                const adjClass = h.adjustment > 0 ? 'text-success' : (h.adjustment < 0 ? 'text-danger' : '');
                                const transferText = h.contra_account ? `→ ${h.contra_account}` : '-';
                                const row = `<tr>
                                    <td>${h.date}</td>
                                    <td class="text-end">${h.old_value.toFixed(2)}</td>
                                    <td class="text-end ${adjClass}">${h.adjustment >= 0 ? '+' : ''}${h.adjustment.toFixed(2)}</td>
                                    <td class="text-end fw-bold">${h.new_value.toFixed(2)}</td>
                                    <td><small>${transferText}</small></td>
                                </tr>`;
                                historyBody.innerHTML += row;
                            });
                        }
                    })
                    .catch(err => {
                        console.error('Error fetching history:', err);
                        document.getElementById('history_body').innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading history</td></tr>';
                    });

                \2'''

new_content = re.sub(pattern, history_fetch_code, content, count=1)

if new_content != content:
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully added Balance History fetch code")
else:
    print("ERROR: Pattern for JS insertion not found")
