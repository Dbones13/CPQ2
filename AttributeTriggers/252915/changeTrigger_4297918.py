additonalCustomDelivCon =  Product.GetContainerByName("MSID_Additional_Custom_Deliverables")
executionCountry = Product.Attr('ACD_Execution_Country').GetValue()
for row in additonalCustomDelivCon.Rows:
    if row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False

Product.Attr("ACD_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')