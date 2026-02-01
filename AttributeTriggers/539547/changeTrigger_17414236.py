gesLocation = TagParserProduct.ParseString('<* Value(SCADA_Ges_Location_Labour) *>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container').Rows
    gesPerc = Product.Attr('SCADA_Labor_GES_%_adc').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))


ScriptExecutor.Execute('PS_Populate_Prices')