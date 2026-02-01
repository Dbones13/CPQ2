def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00
laborRows = Product.GetContainerByName('FDM Engineering Labor Container').Rows
Exp_Stations=Product.Attr('No_of_ Exp_Stations_with_FDM_Maintenance_Station').GetValue()
for row in laborRows:
    try:
        '''lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        if lv_calc_hrs>0 and lv_productivity > 0:
            Trace.Write("test1")
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        	#Modifying for CXCPQ-63514
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        elif lv_calc_hrs==0 and row['ChangeFlag']=='':
            Trace.Write("test2")
            row['Productivity']='1'
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
        #elif row['ChangeFlag']=='1' and lv_calc_hrs==0:
        #    a=row.GetColumnByName('Final Hrs').Value
        #    row['Final Hrs']=a
        #    row.GetColumnByName('ChangeFlag').Value =' '
        elif row['ChangeFlag']=='1':
            if lv_calc_hrs==0 and lv_productivity >=0:
                Trace.Write("test3")
                row['Productivity']='1'
                Trace.Write("lv_calc_hrs"+str(lv_calc_hrs))
                lv_final_hrs = round(lv_calc_hrs * 1)
                Trace.Write("lv_final_hrs"+str(lv_final_hrs))
                row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
                row.GetColumnByName('ChangeFlag').Value =''
        '''
        lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
        lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
        if lv_calc_hrs != lv_prev_calc_hrs:
            lv_final_hrs = round(lv_calc_hrs * lv_productivity)
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
            if lv_calc_hrs == 0:
                row['Productivity']= '1'
            else:
                row['Productivity']= str(lv_productivity)
            row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
    except: pass