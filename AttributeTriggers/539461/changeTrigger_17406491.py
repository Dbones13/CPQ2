gesLocation = TagParserProduct.ParseString('<*CTX( Container(UOC_Labor_Details).Row(1).Column(UOC_Ges_Location_Labour).GetDisplayValue )*>')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE UOC Engineering Labor Container').Rows
    gesPerc = Product.Attr('CE UOC GES Engineer %').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        excludedDeliverables = ['UOC User Requirement Specification', 'UOC Engineering Plan', 'UOC Procure Materials & Services', 'UOC Customer Training', 'UOC Project Close Out Report']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - gesPerc - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
                #row.GetColumnByName('FO Eng 2 % Split').Value = "0"
                #row.GetColumnByName('FO Eng 1 % Split').Value = str(100-(gesPerc))
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
                updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Show_UOC_Error_Deliverables')