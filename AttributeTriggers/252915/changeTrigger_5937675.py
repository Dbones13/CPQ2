container =  Product.GetContainerByName("MSID_Labor_EHPM_HART_IO_Con")
executionCountry = Product.Attr('EHPM_HART_IO_Execution_Country').GetValue()
for row in container.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        row.IsSelected = False
Product.Attr("EHPM_HART_IO_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')