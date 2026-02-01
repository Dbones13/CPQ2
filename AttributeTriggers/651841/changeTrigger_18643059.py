#Attribute 'CE PLC Engineering Execution Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
execYear = TagParserProduct.ParseString('<* Value(CE PLC Engineering Execution Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear