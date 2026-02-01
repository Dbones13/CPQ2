#Populate each container row with the 'Productivity' value - default value only
laborRows = Product.GetContainerByName('MSE_Engineering_Labor_Container')
prod = Product.Attr('MSE_Engineering_Labor_Productivity').GetValue()
updatePrice = 0
Product.ExecuteRulesOnce = True
for row in laborRows.Rows:
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
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_MSE_Labor_Container')
Product.ExecuteRulesOnce = False
Product.Attr('MSE_Engineering_Labor_Productivity').AssignValue('')