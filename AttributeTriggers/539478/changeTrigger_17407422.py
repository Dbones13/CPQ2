#Attribute 'HC900_ACD_GES_%' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('Product.Attr("HC900_Ges_Location_Labour").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('HC900 Additional Custom Deliverables').Rows
    gesPerc = Product.Attr('HC900_ACD_GES_%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_Show_HC900_Error_Deliverables')