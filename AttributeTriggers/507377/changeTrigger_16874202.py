gesLocation = Product.Attr('IS_GES_Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('IS_Labor_Container').Rows
    gesPerc = Product.Attr('IS_Labor_GES_%').GetValue()
    gesPerc=float(gesPerc) if gesPerc else 0

    for row in laborRows:
        if not row.IsSelected:
            continue
        fo_eng_1_split = float(100 - gesPerc - float(row['FO Eng 2 % Split']))
        row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
        if fo_eng_1_split < 0:
            updatePrice = 0
            pass
        else:
            row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
            updatePrice = 1
        #row.IsSelected = False
if updatePrice:
    ScriptExecutor.Execute('PS_IS_Update_Labor_Cost')
ScriptExecutor.Execute('PS_IS_Error_Message')
Product.Attr('IS_Labor_GES_%').AssignValue('')