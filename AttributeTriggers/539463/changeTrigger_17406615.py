#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('Product.Attr("PCD_Ges_Location_Labour").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('PCD Additional Custom Deliverables').Rows
    gesPerc = Product.Attr('PCD_ACD_GES_%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_Show_PCD_Error_Deliverables')