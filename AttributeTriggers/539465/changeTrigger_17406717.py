gesLocation = TagParserProduct.ParseString('<*CTX( Container(RTU_Software_Labor_Container2).Row(1).Column(RTU_GES_Location).GetDisplayValue )*>')

gesPerc = float(Product.Attr('CE RTU GES Engineer %').GetValue())
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('CE RTU Engineering Labor Container').Rows
    for row in laborRows:
        excludedDeliverables = ['RTU FEL Site Visit', 'RTU Procure Materials & Services', 'RTU Customer Training', 'RTU Project Close Out Report']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - gesPerc - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
                updateFlag = 1
#ScriptExecutor.Execute('PS_Show_RTU_Error_Deliverables')
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')