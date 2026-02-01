#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
laborRows = laborCont.Rows
prod = TagParserProduct.ParseString('<* Value(SM_Labor_Productivity) *>')

for row in laborRows:
    if row.IsSelected:
        try:
            calc = float(row.GetColumnByName('Calculated Hrs').Value)
        except:
            calc = 0.00
        if calc > 0:
            row.GetColumnByName('Productivity').Value = prod
            final = calc * float(prod)
            row.GetColumnByName('Final Hrs').Value = str(final)
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborCont.Calculate()
laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
laborRows1 = laborCont1.Rows
prod = TagParserProduct.ParseString('<* Value(SM_Labor_Productivity) *>')

for row in laborRows1:
    if row.IsSelected:
        try:
            calc = float(row.GetColumnByName('Calculated Hrs').Value)
        except:
            calc = 0.00
        if calc > 0:
            row.GetColumnByName('Productivity').Value = prod
            final = calc * float(prod)
            row.GetColumnByName('Final Hrs').Value = str(final)
#ScriptExecutor.Execute('PS_Populate_Prices')