#Attribute 'C300_Addnl_Cust_Del_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('DVM_Additional_Labour_Container').Rows
execYear = Product.Attr('DVM_Project_Additional_Year').GetValue()
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_DVM_Error_Msg')