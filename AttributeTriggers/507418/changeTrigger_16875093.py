#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('PAGA_Labor_Container')
laborRows = laborCont.Rows
prod = Product.Attr('PAGA_Productivity').GetValue()
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
        #row.IsSelected=False
laborCont.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PAGA_Update_Labor_Cost')
Product.ExecuteRulesOnce = False
Product.Attr('PAGA_Productivity').AssignValue('')