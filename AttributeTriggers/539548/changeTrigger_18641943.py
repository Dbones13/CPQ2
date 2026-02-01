traceCon =  Product.GetContainerByName("Trace_Software_Labor_con")
executionCountry = Product.Attr('Trace_Software_Execution_Country').GetValue()
for row in traceCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("Trace_Software_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')
ScriptExecutor.Execute('PS_CalculateMPAPrice')