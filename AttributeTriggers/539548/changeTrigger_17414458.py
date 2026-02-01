CWSRAECon =  Product.GetContainerByName("MSID_Labor_CWS_RAE_Upgrade_con")
executionCountry = Product.Attr('CWS_RAE_Upgrade_Execution_Country').GetValue()
for row in CWSRAECon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("CWS_RAE_Upgrade_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')