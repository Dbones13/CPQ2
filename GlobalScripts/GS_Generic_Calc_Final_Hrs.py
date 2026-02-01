#GS_SM_UpdateFinalHours
def updateFinalHours(laborRows):
	for row in laborRows:
		try:
			lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
			lv_productivity = float(row.GetColumnByName('Productivity').Value)
			if lv_calc_hrs > 0:
				lv_final_hrs = round(lv_calc_hrs * lv_productivity)
				row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
		except Exception, e:
			Trace.Write(str(e))
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':
    laborRows = Product.GetContainerByName('Generic Engineering Labor Container').Rows
    updateFinalHours(laborRows)
    Product.GetContainerByName('Generic Engineering Labor Container').Calculate()