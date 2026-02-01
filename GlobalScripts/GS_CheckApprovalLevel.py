import GS_CommonModule as CM
LOB = CM.getCFValue(Quote, "Booking LOB")
if Quote.OrderStatus.Name == "Preparing" and Quote.Items.Count > 0 and LOB in ['LSS', 'PAS', 'CCC', 'HCP']:
    ScriptExecutor.Execute('GS_ApprovalTabContent', {"Approval": "Getapproval"})