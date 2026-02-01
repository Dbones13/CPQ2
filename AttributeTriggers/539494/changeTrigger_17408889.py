gesLocation = TagParserProduct.ParseString('<* Value(MXPro_GES_Location) *>')
gesPerc = Product.Attr('MXPro_Labor_GES_percent').GetValue()
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('MXPro_Labor_Container ').Rows
    for row in laborRows:
        excludedDeliverables = ['MXProLine Engineering Plan','MXProLine Procure Materials & Services','MXProLine Customer Training','MXProLine Project Close Out Report']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)


ScriptExecutor.Execute('PS_Populate_Prices')