#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('PRMS_Engineering_Labor_Container')
prod = Product.Attr('PRMS_Engineering_Labor_Productivity').GetValue()
updatePrice = 0
Product.ExecuteRulesOnce = True
for row in laborCont.Rows:
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
    ScriptExecutor.Execute('PS_PRMS_Update_Labor_Cost')
Product.ExecuteRulesOnce = False
Product.Attr('PRMS_Engineering_Labor_Productivity').AssignValue('')