#Attribute 'CE LD GES%' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('<*CTX( Container(PMD_Labour_Details).Row(1).Column(PMD_Ges_Location).GetDisplayValue )*>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('PMD Labor Additional Custom Deliverable').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(PMD CE LD GES Engineer %) *>')
    for row in laborRows:
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = gesPerc