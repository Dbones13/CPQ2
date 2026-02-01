cbecCon =  Product.GetContainerByName("MSID_Labor_XP10_Actuator_Upgrade_con")
executionCountry = Product.Attr('XP10_Actuator_Upgrade_Execution_Country').GetValue()
for row in cbecCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("XP10_Actuator_Upgrade_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')