gesLocation = TagParserProduct.ParseString('Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()')
updateFlag = 0

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Experion HS Additional Custom Deliverables').Rows
    gesPerc = Product.Attr('Experion_HS_CD_LD_GES Engineer %').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')