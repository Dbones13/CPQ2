laborAdditional1 = Product.GetContainerByName('PMD Labor Additional Custom Deliverable').Rows
choice11 = TagParserProduct.ParseString('<*Value(PMD Check All Additional)*>')

if choice11 <> '':
    for row1 in laborAdditional1:
        row1.IsSelected = 'Yes'
elif choice11 <> 'Yes': 
    for row1 in laborAdditional1:
        row1.IsSelected = ''