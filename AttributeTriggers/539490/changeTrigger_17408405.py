gesLocation = TagParserProduct.ParseString('<* Value(MX_HC_GES_Location) *>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Experion_mx_labor_Additional_Cust_Deliverables_con').Rows
    gesPerc = Product.Attr('Experion_mx_Labor_GES_percent_adc').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))


ScriptExecutor.Execute('PS_Populate_Prices')