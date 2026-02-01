#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborRows = Product.GetContainerByName('HC900 Engineering Labor Container').Rows

for row in laborRows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
    except:
		continue