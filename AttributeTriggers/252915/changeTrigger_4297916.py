lcnOneTimeUpgradeCon =  Product.GetContainerByName("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
executionCountry = Product.Attr('LCN_Execution_Country').GetValue()
for row in lcnOneTimeUpgradeCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("LCN_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')