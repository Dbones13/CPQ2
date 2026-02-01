#Attribute 'CE PMD Engineering Execution Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PMD Engineering Labor Container').Rows
execYear = TagParserProduct.ParseString('<* Value(CE PMD ACD Execution Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear