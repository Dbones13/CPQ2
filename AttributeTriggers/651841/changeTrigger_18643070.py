#Attribute 'PLC_CD_LD_Engineering_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
execCount = TagParserProduct.ParseString('<*VALUE(PLC_CD_LaborDeliverables_Execution Country)*>')
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCount
        row.GetColumnByName('UpdatedYear').Value = execCount
laborRows.Calculate()