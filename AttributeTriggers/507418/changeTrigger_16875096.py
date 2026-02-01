gesLocation = Product.Attr('PAGA_GES_Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborCont=Product.GetContainerByName('PAGA_Labor_Container')
    laborRows = Product.GetContainerByName('PAGA_Labor_Container').Rows
    gesPerc = Product.Attr('PAGA_GES%').GetValue()
    gesPerc=float(gesPerc) if gesPerc else 0
    deliverables = ["BOM Generation and Ordering"]

    for row in laborRows:
        if not row.IsSelected or row['Deliverable'] in deliverables:
            #row.IsSelected=False
            continue
        fo_eng_1_split = float(100 - gesPerc - float(row['FO Eng 2 % Split']))
        row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
        if fo_eng_1_split < 0:
            updatePrice = 0
            pass
        else:
            row.GetColumnByName('FO Eng 1 % Split').Value = str(fo_eng_1_split)
            updatePrice = 1
        #row.IsSelected=False
    laborCont.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PAGA_Update_Labor_Cost')
ScriptExecutor.Execute('PS_PAGA_Error_Msg')
Product.Attr('PAGA_GES%').AssignValue('')