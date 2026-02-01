#This Script will update the SC_EnabledServiceChkFlg attribute when Enabled Services is configured.
Product.Attr('SC_EnabledServiceChkFlg_New').AssignValue('False')
sc_module1 = Product.GetContainerByName("Service Contract Modules")
if sc_module1.Rows.Count:
    for row in sc_module1.Rows:
        if row.Product.Name == "Enabled Services":
            Product.Attr('SC_EnabledServiceChkFlg_New').AssignValue('True')
            break
