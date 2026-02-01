#Attribute 'C300_Addnl_Cust_Del_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container').Rows
execYear = Product.Attr('C300_Addnl_Cust_Del_Execution_Year').GetValue()
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')