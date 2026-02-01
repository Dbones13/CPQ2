GraphicsCon =  Product.GetContainerByName("MSID_Labor_Graphics_Migration_con")
executionCountry = Product.Attr('Graphics_Migration_Execution_Country').GetValue()
for row in GraphicsCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("Graphics_Migration_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')