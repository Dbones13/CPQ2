xPMCon =  Product.GetContainerByName("MSID_Labor_xPM_to_C300_Migration_Con")
executionCountry = Product.Attr('xPM_to_C300_Migration_Execution_Country').GetValue()
for row in xPMCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("xPM_to_C300_Migration_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')