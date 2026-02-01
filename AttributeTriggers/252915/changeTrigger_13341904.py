fdmCon =  Product.GetContainerByName("MSID_Labor_FDM_Upgrade_Con")
executionCountry = Product.Attr('FDM_Upgrade_Execution_Country').GetValue()
for row in fdmCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("FDM_Upgrade_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')