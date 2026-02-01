#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborCont = Product.GetContainerByName('MIQ Engineering Labor Container')

for row in laborCont.Rows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        if lv_calc_hrs > 0:
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
    except: pass
laborCont.Calculate()