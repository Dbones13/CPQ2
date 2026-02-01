#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborRows = Product.GetContainerByName('PSW_Labor_Container').Rows
for row in laborRows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        if lv_calc_hrs >0 and lv_productivity > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        if lv_calc_hrs==0:
                row.GetColumnByName('Productivity').Value = "1"
    except:
        pass