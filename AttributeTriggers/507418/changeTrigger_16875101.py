gesLocation = TagParserProduct.ParseString('Product.Attr("PAGA_GES_Location").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborCont=Product.GetContainerByName('PAGA_Additional_Labour_Container')
    laborRows = Product.GetContainerByName('PAGA_Additional_Labour_Container').Rows
    gesPerc = Product.Attr('PAGA_Ad_GES%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
        #row.IsSelected=False
    laborCont.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_PAGA_Update_Labor_Cost')
ScriptExecutor.Execute('PS_PAGA_Error_Msg')
Product.Attr('PAGA_Ad_GES%').AssignValue('')