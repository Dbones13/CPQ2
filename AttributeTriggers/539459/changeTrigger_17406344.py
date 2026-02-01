gesLocation = gesLocation = TagParserProduct.ParseString('<*CTX( Container(SM_Labor_Cont).Row(1).Column(GES_Location).GetDisplayValue )*>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container').Rows
    gesPerc = Product.Attr('SM_Labor_GES_%_adc').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))


ScriptExecutor.Execute('PS_Populate_Prices')