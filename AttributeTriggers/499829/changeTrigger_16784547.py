projectManagementCon =  Product.GetContainerByName("Trace_Project_Management_Labor_con")
executionCountry = Product.Attr('PM_Execution_Country').GetValue()
for row in projectManagementCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False

Product.Attr("PM_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')
ScriptExecutor.Execute('PS_CalculateMPAPrice')