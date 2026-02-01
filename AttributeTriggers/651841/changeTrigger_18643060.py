#Attribute 'CE PLC GES%' Change Trigger 
#Populate each container row with the 'GES Eng % Split' value - default value only

gesLocation = TagParserProduct.ParseString('<*CTX( Container(PLC_Labour_Details).Row(1).Column(PLC_Ges_Location).GetDisplayValue )*>')
deliverables = ['CE PLC Engineering Plan', 'CE PLC Procure Materials & Services', 'CE PLC Customer Training', 'CE PLC Project Close Out Report']
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
    gesPerc = TagParserProduct.ParseString('<* Value(CE PLC GES Engineer %) *>')
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected and row['Deliverable'] not in deliverables:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
# if updateFlag:
#     ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')