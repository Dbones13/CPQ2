laborAdditional = Product.GetContainerByName('CE PLC Additional Custom Deliverables').Rows
choice1 = TagParserProduct.ParseString('<* Value(Check All Additional) *>')

if choice1 <> '':
    for row1 in laborAdditional:
        row1.IsSelected = 'Yes'
elif choice1 <> 'Yes': 
    for row1 in laborAdditional:
        row1.IsSelected = ''