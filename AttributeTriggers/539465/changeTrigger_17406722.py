#Attribute 'RTU_CD_LaborDeliverables_Execution Country' Change Trigger 
#Populate each selected container row with the 'Execution country' value
laborRows = Product.GetContainerByName('CE RTU Additional Custom Deliverables')
execCount = TagParserProduct.ParseString('<*VALUE(RTU_CD_LaborDeliverables_Execution Country)*>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCount
        updateFlag = 1
        #row.GetColumnByName('UpdatedYear').Value = execCount
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#laborRows.Calculate()
ScriptExecutor.Execute('PS_Show_RTU_Error_Deliverables')