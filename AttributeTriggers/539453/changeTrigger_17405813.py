#Populate each container row with the 'Productivity' value - default value only
laborCont = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
laborRows = laborCont.Rows
prod = TagParserProduct.ParseString('<* Value(System_Network_Labor_Productivity) *>')
updateFlag = 0
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
            updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')