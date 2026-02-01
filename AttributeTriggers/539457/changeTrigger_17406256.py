def getFloat(var):
    if var:
        return float(var)
    else:
        return 0
gesLocation = Product.Attr('Virtualization_Ges_Location').GetValue()
gesPerc = Product.Attr('Virtualization_Labor_GES_Perct').GetValue()
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Virtualization_Labor_Deliverable').Rows
    for row in laborRows:
        excludedDeliverables = []
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - getFloat(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)

#ScriptExecutor.Execute('PS_Populate_Prices')
#ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')