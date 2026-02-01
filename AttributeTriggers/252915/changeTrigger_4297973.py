ebrCon = Product.GetContainerByName("MSID_Labor_EBR_Con")
executionCountry = Product.Attr('EBR_Execution_Country').GetValue()
for row in ebrCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("EBR_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')
#ScriptExecutor.Execute('PS_PopulateMPAPrice')