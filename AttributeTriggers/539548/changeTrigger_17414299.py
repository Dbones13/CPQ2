elcnCon = Product.GetContainerByName("MSID_Labor_ELCN_Con")
executionCountry = Product.Attr('ELCN_Execution_Country').GetValue()
for row in elcnCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("ELCN_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')
#ScriptExecutor.Execute('PS_PopulateMPAPrice')