saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if saveAction != 'Save' and isR2Qquote:
    smControlGroup = ['PS_SM_Hide_values','OnProductRuleExecutionEnd','PS_SM_Parts_components','PS_SM_CG_Component_Calcs','PS_SM_CG_IOTAs_Calcs','PS_SM_Sys_Cabinets_Qty','PS_License_run','PS_SM_CG_Part_Summary','PS_SM_IO_Cnt_Populate','PS_SM_CG_LI_Part_Summary','PS_Populate_Total_IO_Points']
    for scr in smControlGroup:
        Product.ParseString('<* ExecuteScript({}) *>'.format(scr))