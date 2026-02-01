#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborRows = Product.GetContainerByName('CE PLC Engineering Labor Container').Rows

for row in laborRows:
    try:
        calc = float(row.GetColumnByName('Calculated Hrs').Value)
        prod = float(row.GetColumnByName('Productivity').Value)
        final = round(calc * prod)
        row.GetColumnByName('Final Hrs').Value = str(final)
    except:
        pass
Product.Attr('PERF_ExecuteScriptsLabor').AssignValue('')