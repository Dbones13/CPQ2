#Attribute 'C300_Additional_Custom_Deliverables_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container').Rows
execCountry = Product.Attr('C300_Addnl_Cust_Del_Execution_Country').GetValue()
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')