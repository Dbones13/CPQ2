#Attribute 'CE PLC Engineering Execution Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(CE PLC Engineering Execution Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry