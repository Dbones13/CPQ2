gesLocation = TagParserProduct.ParseString('<* Value(MX_HC_GES_Location) *>')
gesPerc = Product.Attr('Experion_mx_Labor_GES_percent').GetValue()
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Experion_mx_Labor_Container ').Rows
    for row in laborRows:
        excludedDeliverables = ['Experion MX Engineering Plan','Experion MX Procure Materials & Services','Experion MX Customer Training','Experion MX Project Close Out Report']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)


ScriptExecutor.Execute('PS_Populate_Prices')