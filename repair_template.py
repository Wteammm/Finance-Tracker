# Emergency repair for balance_sheet.html corruption
# Only fix the Edit Modal section

import re

template_path = r'c:\Users\kalis\.gemini\antigravity\scratch\Finance_Tracker\templates\balance_sheet.html'

# Read current broken file
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the edit modal start
modal_start = content.find('\u003c!-- Edit Item Modal --\u003e')
if modal_start == -1:
    print("ERROR: Can't find Edit Modal")
    exit(1)

# Find the script section start (after all modals)
script_start = content.find('\u003cscript\u003e', modal_start)
if script_start == -1:
    print("ERROR: Can't find script section")
    exit(1)

# Replace the broken modal section with the correct one
correct_edit_modal = '''    \u003c!-- Edit Item Modal --\u003e
    \u003cdiv class="modal fade" id="editModal" tabindex="-1" aria-hidden="true"\u003e
        \u003cdiv class="modal-dialog"\u003e
            \u003cdiv class="modal-content"\u003e
                \u003cdiv class="modal-header"\u003e
                    \u003ch5 class="modal-title"\u003eEdit Item\u003c/h5\u003e
                    \u003cbutton type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"\u003e\u003c/button\u003e
                \u003c/div\u003e
                \u003cdiv class="modal-body"\u003e
                    \u003cform id="editForm" method="POST"\u003e
                        \u003cdiv class="mb-3"\u003e
                            \u003clabel class="form-label"\u003eName\u003c/label\u003e
                            \u003cinput type="text" class="form-control" name="name" id="edit_name" required\u003e
                        \u003c/div\u003e
                        \u003cdiv class="mb-3"\u003e
                            \u003clabel class="form-label"\u003eLiquidity Tier\u003c/label\u003e
                            \u003cselect class="form-select" name="liquidity_tier" id="edit_tier"\u003e
                                \u003coption value=""\u003eNone / Not Applicable\u003c/option\u003e
                                \u003coption value="High"\u003eHigh\u003c/option\u003e
                                \u003coption value="Medium"\u003eMedium\u003c/option\u003e
                                \u003coption value="Low"\u003eLow\u003c/option\u003e
                            \u003c/select\u003e
                        \u003c/div\u003e
                        \u003c!-- BF / Adjustment / CF Layout --\u003e
                        \u003cdiv class="row g-2 mb-3"\u003e
                            \u003cdiv class="col-md-4"\u003e
                                \u003clabel class="form-label small text-muted"\u003eBrought Forward (BF)\u003c/label\u003e
                                \u003cinput type="number" step="0.01" class="form-control" id="edit_old_value" name="old_value" title="Original Value"\u003e
                            \u003c/div\u003e
                            \u003cdiv class="col-md-4"\u003e
                                \u003clabel class="form-label small text-muted"\u003eAdjustment (+/-)\u003c/label\u003e
                                \u003cinput type="number" step="0.01" class="form-control" id="edit_adjustment" placeholder="+/-"\u003e
                            \u003c/div\u003e
                            \u003cdiv class="col-md-4"\u003e
                                \u003clabel class="form-label fw-bold"\u003eCarried Forward (CF)\u003c/label\u003e
                                \u003cinput type="number" step="0.01" class="form-control fw-bold" name="value" id="edit_value" required\u003e
                            \u003c/div\u003e
                        \u003c/div\u003e
                        \u003cdiv class="form-text mt-0 mb-3 small fst-italic"\u003eCF automatically updates based on Adjustment.\u003c/div\u003e

                        \u003c!-- Linked Transactions (Collapsible) --\u003e
                        \u003cdiv class="mb-3"\u003e
                            \u003cbutton class="btn btn-sm btn-outline-secondary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#transactionHistory" aria-expanded="false"\u003e
                                \u003ci class="bi bi-clock-history"\u003e\u003c/i\u003e Show Linked Transactions
                            \u003c/button\u003e
                            \u003cdiv class="collapse mt-2" id="transactionHistory"\u003e
                                \u003cdiv class="card card-body p-2 bg-light"\u003e
                                    \u003cdiv class="table-responsive" style="max-height: 200px;"\u003e
                                        \u003ctable class="table table-sm table-borderless small mb-0" id="txn_table"\u003e
                                            \u003cthead\u003e
                                                \u003ctr\u003e
                                                    \u003cth\u003eDate\u003c/th\u003e
                                                    \u003cth\u003eDesc\u003c/th\u003e
                                                    \u003cth class="text-end"\u003eAmt\u003c/th\u003e
                                                \u003c/tr\u003e
                                            \u003c/thead\u003e
                                            \u003ctbody id="txn_body"\u003e
                                                \u003ctr\u003e
                                                    \u003ctd colspan="3" class="text-center"\u003eLoading...\u003c/td\u003e
                                                \u003c/tr\u003e
                                            \u003c/tbody\u003e
                                        \u003c/table\u003e
                                    \u003c/div\u003e
                                \u003c/div\u003e
                            \u003c/div\u003e
                        \u003c/div\u003e

                        \u003chr\u003e
                        \u003ch6 class="mb-3 text-primary"\u003e\u003ci class="bi bi-arrow-left-right"\u003e\u003c/i\u003e Contra / Transfer (Optional)\u003c/h6\u003e
                        \u003cdiv class="mb-3 bg-light p-3 rounded"\u003e
                            \u003cdiv class="form-check form-switch mb-2"\u003e
                                \u003cinput class="form-check-input" type="checkbox" id="enable_contra" name="enable_contra"\u003e
                                \u003clabel class="form-check-label fw-bold" for="enable_contra"\u003eOffset / Contra with another account?\u003c/label\u003e
                            \u003c/div\u003e

                            \u003cdiv id="contra_fields" style="display:none;"\u003e
                                \u003cdiv class="mb-3"\u003e
                                    \u003clabel class="form-label"\u003eContra Account (Source/Destination)\u003c/label\u003e
                                    \u003cselect class="form-select" name="contra_item_id" id="contra_select"\u003e
                                        \u003coption value=""\u003eSelect Account...\u003c/option\u003e
                                        \u003c!-- Populated by JS --\u003e
                                    \u003c/select\u003e
                                    \u003cdiv class="form-text small mt-2"\u003e
                                        \u003ci class="bi bi-info-circle"\u003e\u003c/i\u003e The difference (New Value - Old Value) will be \u003cstrong\u003ededucted\u003c/strong\u003e from this account.
                                    \u003c/div\u003e
                                \u003c/div\u003e
                            \u003c/div\u003e
                        \u003c/div\u003e
                        \u003cdiv class="text-end"\u003e
                            \u003cbutton type="submit" class="btn btn-primary"\u003eSave Changes\u003c/button\u003e
                        \u003c/div\u003e
                    \u003c/form\u003e
                \u003c/div\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/div\u003e
\u003c/div\u003e

\u003c!-- Custom Context Menu --\u003e
\u003cdiv id="contextMenu" class="dropdown-menu" style="display:none; position:fixed; z-index:10000; box-shadow: 0 0 10px rgba(0,0,0,0.2);"\u003e
    \u003ca class="dropdown-item" href="#" id="ctxEdit"\u003e\u003ci class="bi bi-pencil me-2"\u003e\u003c/i\u003eEdit\u003c/a\u003e
    \u003ca class="dropdown-item text-danger" href="#" id="ctxDelete"\u003e\u003ci class="bi bi-trash me-2"\u003e\u003c/i\u003eDelete\u003c/a\u003e
\u003c/div\u003e

'''

# Replace the broken section
new_content = content[:modal_start] + correct_edit_modal + content[script_start:]

# Write fixed file
with open(template_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed balance_sheet.html - Edit Modal section restored")
