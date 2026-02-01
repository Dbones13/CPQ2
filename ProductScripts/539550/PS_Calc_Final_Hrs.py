#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborRows = Product.GetContainerByName('PMD Engineering Labor Container').Rows

for row in laborRows:
    calc_name = (row.GetColumnByName("Deliverable").Value)
    if calc_name != "PMD Cut Over Procedure":
        try:
            calc = float(row.GetColumnByName('Calculated Hrs').Value)
            prod = float(row.GetColumnByName('Productivity').Value)
            final = round(calc * prod)
            row.GetColumnByName('Final Hrs').Value = str(final)
        except:
            pass