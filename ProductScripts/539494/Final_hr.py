laborRows = Product.GetContainerByName('MXPro_Labor_Container').Rows
def getFloat(Var):
   if Var:
       return float(Var)
   return 0

for row in laborRows:
    lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
    lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
    #Trace.Write(str(lv_calc_hrs) +"#############"+ str(lv_productivity))
    if lv_calc_hrs >0:
        lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
'''for row in laborRows:
    try:
        if float(row.GetColumnByName('Calculated Hrs').Value) != 0.00:
            lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
            lv_productivity = float(row.GetColumnByName('Productivity').Value)
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
    except:
        continue
'''