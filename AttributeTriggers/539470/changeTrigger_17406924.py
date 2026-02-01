def getFloat(val):
    res = 0
    if val:
        try:
            res = float(val)
        except ValueError:
            res = 0
    return res
gesLocation = Product.Attr('DVM_GES_Location').GetValue()
updateFlag = 0
if gesLocation not in ("None", ""):
    laborRows = Product.GetContainerByName('DVM_Additional_Labour_Container').Rows
    gesPerc = Product.Attr('DVM_Project_Additional_GES').GetValue()
    for row in laborRows:
        gesPerc=getFloat(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100 - gesPerc)
            updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')