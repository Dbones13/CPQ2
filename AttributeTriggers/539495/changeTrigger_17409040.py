#Attribute 'CE LD GES%' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('<*CTX( Container(PLC_Labour_Details).Row(1).Column(PLC_Ges_Location).GetDisplayValue )*>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE PLC Additional Custom Deliverables').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(CE LD GES Engineer %) *>')
    for row in laborRows:
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = gesPerc