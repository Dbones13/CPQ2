#PS_TM_Calculate_Labor_Hours
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
    TM_Devices_Cont = Product.GetContainerByName('Terminal_Devices_Scope')
    TM_Workflow_Cont = Product.GetContainerByName('Terminal_Workflow_Scope')
    TM_BSI_Cont = Product.GetContainerByName('Terminal_SAP_ERP_BSI_Interface_Scope')
        
    if TM_Workflow_Cont.Rows.Count>0:
        for wrow in TM_Workflow_Cont.Rows:
            calc_name_dict[wrow.GetColumnByName("Deliverable").Value] = wrow.GetColumnByName("CalculatedHrs_Formula").Value
    
    if TM_Devices_Cont.Rows.Count>0:
        for drow in TM_Devices_Cont.Rows:
            calc_name_dict[drow.GetColumnByName("Deliverable").Value] = drow.GetColumnByName("CalculatedHrs_Formula").Value
    
    if TM_BSI_Cont.Rows.Count>0:
        for brow in TM_BSI_Cont.Rows:
            calc_name_dict[brow.GetColumnByName("Deliverable").Value] = brow.GetColumnByName("CalculatedHrs_Formula").Value
    lv_CHrs_Tot=0
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_name_dict.keys():
            lv_CalHrs = calc_name_dict[row.GetColumnByName("Deliverable").Value]
            row.GetColumnByName("CalculatedHrs_Script").Value = lv_CalHrs
            row.Product.ApplyRules()
            row.Calculate()

    laborCont.Calculate()
    Product.ExecuteRulesOnce = True