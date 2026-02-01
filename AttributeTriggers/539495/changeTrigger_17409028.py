#Attribute 'CE PLC GES%' Change Trigger 
#Populate each container row with the 'GES Eng % Split' value - default value only

gesLocation = TagParserProduct.ParseString('<*CTX( Container(PLC_Labour_Details).Row(1).Column(PLC_Ges_Location).GetDisplayValue )*>')
deliverables = ['CE PLC Engineering Plan', 'CE PLC Procure Materials & Services', 'CE PLC Customer Training', 'CE PLC Project Close Out Report']

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(CE PLC GES Engineer %) *>')
    for row in laborRows:
        if row.IsSelected and row['Deliverable'] not in deliverables:
            row.GetColumnByName('GES Eng % Split').Value = gesPerc