#Updates each container row with the new Final Hrs (in case calculated hours has changed)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00
laborRows = Product.GetContainerByName('CE RTU Engineering Labor Container').Rows
for row in laborRows:
    try:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
        if lv_calc_hrs != lv_prev_calc_hrs:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
            if lv_calc_hrs == 0:
                row['Productivity']= '1'
            else:
                row['Productivity']= str(lv_productivity)
            row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
    except Exception, e:
        Trace.Write(str(e))