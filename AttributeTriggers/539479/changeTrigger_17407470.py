gesLocation = Product.Attr('C300_GES_Location').GetValue()
updateFlag = 0
if gesLocation not in ("None", ""):
    laborRows = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container').Rows
    gesPerc = Product.Attr('C300_Addnl_Cust_Del_GES_Percentage').GetValue()
    gesPerc=float(gesPerc)

    for row in laborRows:
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100 - gesPerc)
            updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')