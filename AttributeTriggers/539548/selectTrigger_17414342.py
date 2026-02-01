contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
val = Product.Attr('MSID_Is_FTE_based_System_already_installed_on_Site').GetValue()

for row in contObj.Rows:
    try:
        if row.Product.Name in ['3rd Party PLC to ControlEdge PLC/UOC']:
            row.Product.Attr('PLC_UOC_labor_parameter_var_17_CommonQuestions').AssignValue(val)
        row['MSID_Is_FTE_based_System_already_installed_on_Site'] = val
        row.Product.Attr('MSID_Is_FTE_based_System_already_installed_on_Site').SelectValue(val)
        
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()