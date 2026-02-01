#Populate each container row with the 'Productivity' value - default value only
laborRows = Product.GetContainerByName('PMD Engineering Labor Container').Rows
prod = TagParserProduct.ParseString('<* Value(PMD Engineering Productivity) *>')
# Removed CXCPQ-25187 fix - Broke functionality. Instead use Min/Max values within the attribute itself, under Additional Attribute Definition
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