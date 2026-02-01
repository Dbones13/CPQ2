#Attribute 'CE LD GES%' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('<*CTX( Container(PLC_Labour_Details).Row(1).Column(PLC_Ges_Location).GetDisplayValue )*>')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE PLC Additional Custom Deliverables').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(CE LD GES Engineer %) *>')
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
# if updateFlag:
#     ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')