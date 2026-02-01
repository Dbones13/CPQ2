container =  Product.GetContainerByName("MSID_Labor_TPS_TO_EXPERION_Con")
executionCountry = Product.Attr('TPS_TO_EXPERION_Execution_Country').GetValue()
for row in container.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("TPS_TO_EXPERION_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')