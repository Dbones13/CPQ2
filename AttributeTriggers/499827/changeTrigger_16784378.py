#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('Labor_Container')
laborRows = laborCont.Rows
prod = TagParserProduct.ParseString('<* Value(Labor_Productivity) *>')
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        try:
            calc = float(row.GetColumnByName('Calculated Hrs').Value)
        except:
            calc = 0.00
        if calc > 0:
            updatePrice = 1
            row.GetColumnByName('Productivity').Value = prod
            final = calc * float(prod)
            row.GetColumnByName('Final Hrs').Value = str(final)
            row.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_Labor_Container')
#laborCont.Calculate()