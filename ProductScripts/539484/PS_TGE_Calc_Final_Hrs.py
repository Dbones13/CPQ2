def getFloat(val):
	if val:
		return float(val)
	return 0.0
#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborCont = Product.GetContainerByName('TGE_Engineering_Labor_Container')
for row in laborCont.Rows:
    try:
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        if lv_calc_hrs >0 and lv_productivity > 0:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        if lv_calc_hrs==0:
            row.GetColumnByName('Productivity').Value = "1"
    except Exception as e:
        Log.Write(str(e))
laborCont.Calculate()