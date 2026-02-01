#Populate each container row with the 'Productivity' value - default value only
laborRows = Product.GetContainerByName('TGE_Engineering_Labor_Container')
prod = Product.Attr('TGE_Productivity').GetValue()
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
    ScriptExecutor.Execute('PS_Populate_TGE_Labor_Price_Cost')
Product.ExecuteRulesOnce = False
Product.Attr('TGE_Productivity').AssignValue('')