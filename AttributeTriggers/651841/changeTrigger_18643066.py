laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
choice = TagParserProduct.ParseString('<* Value(Check All) *>')

if choice <> '':
    for row in laborRows:
        row.IsSelected = 'Yes'
elif choice <> 'Yes': 
    for row in laborRows:
        row.IsSelected = ''