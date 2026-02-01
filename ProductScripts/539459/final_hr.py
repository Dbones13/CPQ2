tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Labor Deliverables' in tabs:
    laborRows = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container').Rows
    for row in laborRows:
        try:
            lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
            lv_productivity = float(row.GetColumnByName('Productivity').Value)
            if lv_calc_hrs > 0:
                lv_final_hrs = round(lv_calc_hrs * lv_productivity)
                row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        except Exception, e:
            Trace.Write(str(e))