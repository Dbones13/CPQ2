gesLocation = TagParserProduct.ParseString('Product.Attr("LMS_GES_Location").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('LMS_Additional_Labor_Container')
    gesPerc = Product.Attr('LMS_Ad_GES%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
            #row.IsSelected=False
    laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_LMS_Update_Labor_Cost')
ScriptExecutor.Execute('PS_LMS_Error_Message')
Product.Attr('LMS_Ad_GES%').AssignValue('')