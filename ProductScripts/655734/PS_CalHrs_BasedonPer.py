def is_float(lv_fl):
    if lv_fl!='':
        return float(lv_fl)
    else:
        return 0.0
scope = Product.Attr('CE_Scope_Choices').GetValue()
if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':

    Product.ExecuteRulesOnce = True
    calc_name_dict = {}
    laborCont = Product.GetContainerByName('Terminal Engineering Labor Container')    
    #Get list of all deliverables to consider in calculated hrs for TM Infrastructure Issues ,TM Product Patches and Upgrade and TM Engineering Management Hours
    tble_data = SqlHelper.GetList("SELECT Deliverable FROM TERMINAL_ENGINEERING_DELIVERABLES WHERE  Include_In_InfraIss_PPU_EM_Hrs = 'Y'")
    lv_list=[]
    for rw in tble_data:
        lv_list.append(rw.Deliverable)
    lv_CHrs_Tot=0.0
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        calc = is_float(row.GetColumnByName('Final Hrs').Value) #Get the sum of final hours and apply %
        if deliverable in lv_list: #calculate total hours of the deliverables in the list
            lv_CHrs_Tot=lv_CHrs_Tot+calc

    #Trace.Write('lv_CHrs_Tot:'+ str(lv_CHrs_Tot))
    calc=0
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable =='TM Infrastructure Issues':
            calc = is_float(lv_CHrs_Tot*10/100)
            row.GetColumnByName('CalculatedHrs_Script').Value=str(calc)
        elif deliverable=='TM Product Patches and Upgrade':
            calc = is_float(lv_CHrs_Tot*7.5/100)
            row.GetColumnByName('CalculatedHrs_Script').Value=str(calc)
        elif deliverable=='TM Engineering Management Hours':
            calc = is_float(lv_CHrs_Tot*8/100)
            row.GetColumnByName('CalculatedHrs_Script').Value=str(calc)
        row.Product.ApplyRules()
        row.Calculate()
    laborCont.Calculate()
    Product.ExecuteRulesOnce = False

#Updates each container row with the new Final Hrs (in case calculated hours has changed)
laborCont = Product.GetContainerByName('Terminal Engineering Labor Container')
laborRows = laborCont.Rows

for row in laborRows:
    try:
        lv_calc_hrs = float(row.GetColumnByName('Calculated Hrs').Value)
        lv_productivity = float(row.GetColumnByName('Productivity').Value)
        lv_final_hrs = round(lv_calc_hrs * lv_productivity)
        if lv_calc_hrs > 0:
            row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
    except:
        pass
laborCont.Calculate()