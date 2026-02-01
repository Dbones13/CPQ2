def getFloat(Var):
    if Var:
        return float(Var)
    return 0

if Product.Name == "Virtualization System":
    laborRows = Product.GetContainerByName('Virtualization_Labor_Deliverable').Rows

    for row in laborRows:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        if lv_calc_hrs >0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)