gesLocation = gesLocation = TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Row(1).Column(GES_Location).GetDisplayValue )*>')
gesPerc = Product.Attr('Project_GES_%').GetValue()
updateFlag = 1
if gesLocation <> "None":
    laborCont = Product.GetContainerByName('Project_management_Labor_Container')
    for row in laborCont.Rows:
        excludedDeliverables = ['']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                updateFlag = 0
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
            row.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_PM_Labor_Container')