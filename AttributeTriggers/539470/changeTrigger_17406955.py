gesLocation = Product.Attr('DVM_GES_Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('DVM_Engineering_Labor_Container').Rows
    gesPerc = Product.Attr('DVM_Engineering_Labor_GES').GetValue()
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
#if updatePrice:
#    ScriptExecutor.Execute('PS_Refresh_DVM_Labor_Container')