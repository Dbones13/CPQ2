gesLocation = Product.Attr('C300_GES_Location').GetValue()
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('C300_Engineering_Labor_Container').Rows
    gesPerc = Product.Attr('C300_Engineering_GES_Percentage').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        excludedDeliverables = ['C300 User Requirement Specification','C300 Engineering Plan','C300 Procure Materials & Services','C300 Customer Training']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
                #row.GetColumnByName('FO Eng 2 % Split').Value = "0"
                #row.GetColumnByName('FO Eng 1 % Split').Value = str(100-(gesPerc))
            else:
                updateFlag = 1
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)

if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_C300_Labor_Container')