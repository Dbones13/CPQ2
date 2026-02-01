QCRAECon =  Product.GetContainerByName("MSID_Labor_QCS_RAE_Upgrade_con")
executionCountry = Product.Attr('QCS_RAE_Upgrade_Execution_Country').GetValue()
for row in QCRAECon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("QCS_RAE_Upgrade_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')