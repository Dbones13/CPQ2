CDActuatorCon =  Product.GetContainerByName("MSID_Labor_CD_Actuator_con")
executionCountry = Product.Attr('CD_Actuator_Execution_Country').GetValue()
for row in CDActuatorCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("CD_Actuator_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')