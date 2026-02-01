#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('C300_Engineering_Labor_Container')
laborRows = laborCont.Rows
prod = Product.Attr('C300_Engineering_Productivity').GetValue()
updatePrice = 0
Product.ExecuteRulesOnce = True
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
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_C300_Labor_Container')
Product.ExecuteRulesOnce = False