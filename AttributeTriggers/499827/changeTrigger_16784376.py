gesLocation = gesLocation = TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Row(1).Column(GES_Location).GetDisplayValue )*>')
gesPerc = Product.Attr('PLE_GES_%').GetValue()
updatePrice = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('PLE_Labor_Container').Rows
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                updatePrice = 0
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
                updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_PLE_Labor_Container')