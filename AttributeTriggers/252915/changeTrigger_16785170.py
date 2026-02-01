fscsmioCon =  Product.GetContainerByName("MSID_Labor_FSCtoSM_IO_con")
executionCountry = Product.Attr('FSCtoSM_IO_Execution_Country').GetValue()
for row in fscsmioCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("FSCtoSM_IO_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')