#Populate each container row with the 'Productivity' value - default value only
laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows
prod = TagParserProduct.ParseString('<* Value(CE PLC Engineering Productivity) *>')

for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Productivity').Value = prod
for row in laborRows:
    try:
        calc = float(row.GetColumnByName('Calculated Hrs').Value)
        prod = float(row.GetColumnByName('Productivity').Value)
        final = calc * prod
    except: continue
    row.GetColumnByName('Final Hrs').Value = str(final)