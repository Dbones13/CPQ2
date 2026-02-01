#Attribute 'CN900_CD_LD_GES Engineer %' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('<*CTX( Container(CN900_Labor_Details).Row(1).Column(CN900_Ges_Location_Labour).GetDisplayValue )*>')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE CN900 Additional Custom Deliverables').Rows
    gesPerc = Product.Attr('CN900_CD_LD_GES Engineer %').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Show_UOC_Error_Deliverables')