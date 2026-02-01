gesLocation = gesLocation = TagParserProduct.ParseString('<*CTX( Container(SM_Labor_Cont).Row(1).Column(GES_Location).GetDisplayValue )*>')
gesPerc = Product.Attr('SM_Labor_GES_%').GetValue()
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows
    for row in laborRows:
        excludedDeliverables = ['SSE User Requirement Specification', 'SSE Engineering Plan', 'SSE Customer Training for Safety System', 'SSE Close Out Report', 'SSE Procure Material & Services']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container').Rows
    for row in laborRows:
        excludedDeliverables = ['SSE User Requirement Specification', 'SSE Engineering Plan', 'SSE Customer Training for Safety System', 'SSE Close Out Report', 'SSE Procure Material & Services']
        if row.IsSelected and row['Deliverable'] not in excludedDeliverables:
            fo_eng_1_split = float(100 - float(gesPerc) - float(row['FO Eng 2 % Split']))
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            if fo_eng_1_split < 0:
                pass
            else:
                row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)

ScriptExecutor.Execute('PS_Populate_Prices')
#ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')