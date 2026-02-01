gesLocation = TagParserProduct.ParseString('<* Value(Experion_HS_Ges_Location_Labour) *>')
updateFlag = 0
if gesLocation <> "None":

    laborRows = Product.GetContainerByName('Hardware Engineering Labour Container').Rows


    gesPerc = Product.Attr('Hardware_Engineering_GES_%').GetValue()

    for row in laborRows:
        gesPerc=float(gesPerc)
        excludedDeliverables = ['SHE Engineering Plan', 'SHE Procure Materials & Services']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
                #row.GetColumnByName('FO Eng 2 % Split').Value = "0"
                #row.GetColumnByName('FO Eng 1 % Split').Value = str(100-(gesPerc))
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
                updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')