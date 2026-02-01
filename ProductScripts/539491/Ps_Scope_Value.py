scope = Product.Attr('Scope').GetValue()
msid_scope = scope if scope else Session["Scope"]

contObj = Product.GetContainerByName('LSS_PLC_connection_transpose')
if contObj.Rows.Count > 0:
    for row in contObj.Rows:
        row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)

contObj = Product.GetContainerByName('LSS_UOC_connection_transpose')
if contObj.Rows.Count > 0:
    for row in contObj.Rows:
        row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)