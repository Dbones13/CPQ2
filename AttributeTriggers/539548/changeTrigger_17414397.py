lmCon =  Product.GetContainerByName("MSID_Labor_LM_to_ELMM_Con")
executionCountry = Product.Attr('LM_to_ELMM_Execution_Country').GetValue()
for row in lmCon.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
        row["Execution_Country"] = executionCountry
        #row.IsSelected = False
Product.Attr("LM_to_ELMM_Execution_Country").SelectDisplayValue('')
ScriptExecutor.Execute('PS_PopulateGESCost')