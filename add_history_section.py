import re

# Read the template file
template_path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the location right before the <hr> after transaction history
marker = '                        </div>\r\n\r\n                        <hr>'

history_section = '''                        </div>

                        <!-- Balance Changes History (Collapsible) -->
                        <div class="mb-3">
                            <button class="btn btn-sm btn-outline-primary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#balanceHistory" aria-expanded="false">
                                <i class="bi bi-file-text"></i> Show Balance Changes History
                            </button>
                            <div class="collapse mt-2" id="balanceHistory">
                                <div class="card card-body p-2 bg-light">
                                    <div class="table-responsive" style="max-height: 250px;">
                                        <table class="table table-sm table-borderless small mb-0" id="history_table">
                                            <thead>
                                                <tr>
                                                    <th>Date</th>
                                                    <th class="text-end">Old</th>
                                                    <th class="text-end">Adj</th>
                                                    <th class="text-end">New</th>
                                                    <th>Transfer</th>
                                                </tr>
                                            </thead>
                                            <tbody id="history_body">
                                                <tr>
                                                    <td colspan="5" class="text-center">Loading...</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr>'''

if marker in content:
    content = content.replace(marker, history_section, 1)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added Balance Changes History section")
else:
    print("ERROR: Marker not found in template")
