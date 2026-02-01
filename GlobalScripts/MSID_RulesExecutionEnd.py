msidContainer = Product.GetContainerByName('MSID_Product_Container').Rows
scopeChoices = Product.Attr('MIgration_Scope_Choices').GetValue()
equipmentInstall = Product.Attr('LSS_Will_Honeywell_perform_equipment_installation').GetValue()
#paramterVar = Product.Attr('PLC_UOC_labor_parameter_var_16').GetValue()
for row in msidContainer:
    #PLC_UOC_labor_parameter_var_16
    if row['Product Name'] == '3rd Party PLC to ControlEdge PLC/UOC' and scopeChoices in ('LABOR', 'HW/SW/LABOR'):
        Product.Attr('PLC_UOC_labor_parameter_var_16').AssignValue(equipmentInstall)
        Trace.Write(equipmentInstall)
        #Trace.Write(paramterVar)
        Trace.Write(row['Product Name'])