opmEngineeringCon =  Product.GetContainerByName("MSID_Labor_OPM_Engineering")
executionCountry = Product.Attr('OPM_Execution_Country').GetValue()
for row in opmEngineeringCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("OPM_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')