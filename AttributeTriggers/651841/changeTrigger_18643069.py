#Attribute 'PLC_CD_LD_Engineering_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
execYear = TagParserProduct.ParseString('<*VALUE(PLC_CD_LD_Engineering_Execution_Year)*>')
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
laborRows.Calculate()