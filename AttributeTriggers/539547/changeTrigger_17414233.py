gesLocation = TagParserProduct.ParseString('<* Value(SCADA_Ges_Location_Labour) *>')
gesPerc = Product.Attr('SCADA_Labor_GES_%').GetValue()
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('SCADA_Engineering_Labor_Container').Rows
    for row in laborRows:
        excludedDeliverables = []
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)


ScriptExecutor.Execute('PS_Populate_Prices')
#ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')