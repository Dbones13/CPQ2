gesLocation = TagParserProduct.ParseString('Product.Attr("MSC GES Location").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('MSC_Additional_Labour_Container')
    gesPerc = Product.Attr('MSC_Addi_Labor_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
            #row.IsSelected=False
    laborRows.Calculate()

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
#ScriptExecutor.Execute('Show_Experion_Ent_Sys_Error_Deliverables')
Product.Attr('MSC_Addi_Labor_GES_%').AssignValue('')