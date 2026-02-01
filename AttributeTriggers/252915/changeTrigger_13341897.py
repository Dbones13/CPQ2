fsctosmCon =  Product.GetContainerByName("MSID_Labor_FSC_to_SM_con")
executionCountry = Product.Attr('FSC_to_SM_Execution_Country').GetValue()
for row in fsctosmCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("FSC_to_SM_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')