def getContainer(Name):
    return Product.GetContainerByName(Name)

isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    ScriptExecutor.Execute('PS_LaborHoursModule')
    ScriptExecutor.Execute('Populate_LaborDeliverables')
    ScriptExecutor.Execute('PS_PopulateGESCost')
    ScriptExecutor.Execute('PS_CalculateMPAPrice')
    ScriptExecutor.Execute('PS_Add_to_Quote_2')
    ScriptExecutor.Execute('PS_Populate_Quote')