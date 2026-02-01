#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborCont = Product.GetContainerByName('Terminal Engineering Labor Container')
laborRows = laborCont.Rows

for row in laborRows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
    except:
        pass
laborCont.Calculate()