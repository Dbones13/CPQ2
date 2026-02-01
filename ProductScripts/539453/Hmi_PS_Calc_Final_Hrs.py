#Updates each container row with the new Final Hrs (in case calculated hours has changed)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00
laborRows = Product.GetContainerByName('HMI_Engineering_Labor_Container')
for row in laborRows.Rows :
    try:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
        if lv_calc_hrs != lv_prev_calc_hrs and lv_calc_hrs > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
            if lv_calc_hrs == 0:
                row['Productivity']= '1'
            else:
                row['Productivity']= str(lv_productivity)
            row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
    except Exception, e:
        Trace.Write(str(e))
laborRows.Calculate()

#Updates each container row with the new Final Hrs (in case calculated hours has changed)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00
laborCont2 = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
for row in laborCont2.Rows:
    try:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
        if lv_calc_hrs != lv_prev_calc_hrs and lv_calc_hrs > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
            if lv_calc_hrs == 0:
                row['Productivity']= '1'
            else:
                row['Productivity']= str(lv_productivity)
            row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
    except Exception, e:
        Trace.Write(str(e))
laborCont2.Calculate()

#Updates each container row with the new Final Hrs (in case calculated hours has changed)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00
laborCont3 = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
for row in laborCont3.Rows :
    try:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
        if lv_calc_hrs != lv_prev_calc_hrs and lv_calc_hrs > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
            if lv_calc_hrs == 0:
                row['Productivity']= '1'
            else:
                row['Productivity']= str(lv_productivity)
            row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
    except Exception, e:
        Trace.Write(str(e))
laborCont3.Calculate()