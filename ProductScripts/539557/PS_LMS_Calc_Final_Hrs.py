#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborCont = Product.GetContainerByName('LMS_Labor_Container')
for row in laborCont.Rows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        if lv_calc_hrs >0 and lv_productivity > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        if lv_calc_hrs==0:
            row.GetColumnByName('Productivity').Value = "1"
    except Exception, e:
        Trace.Write(str(e))
laborCont.Calculate()