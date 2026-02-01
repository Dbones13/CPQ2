cbecCon =  Product.GetContainerByName("MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
executionCountry = Product.Attr('CB-EC_Upgrade_to_C300-UHIO_Execution_Country').GetValue()
for row in cbecCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("CB-EC_Upgrade_to_C300-UHIO_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')