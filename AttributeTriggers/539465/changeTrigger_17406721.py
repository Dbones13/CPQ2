gesLocation = TagParserProduct.ParseString('<*CTX( Container(RTU_Software_Labor_Container2).Row(1).Column(RTU_GES_Location).GetDisplayValue )*>')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE RTU Additional Custom Deliverables').Rows
    gesPerc = Product.Attr('RTU_CD_LD_GES Engineer %').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')