gesLocation = TagParserProduct.ParseString('Product.Attr("PSW_GES_Location").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('PSW_Additional_Labor_Container')
    gesPerc = Product.Attr('PSW_Additional_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
        #row.IsSelected=False
    laborRows.Calculate()

if updateFlag:
     ScriptExecutor.Execute('PS_PSW_Update_Labor_Cost')
ScriptExecutor.Execute('PS_Error_msg')
Product.Attr('PSW_Additional_GES_%').AssignValue('')