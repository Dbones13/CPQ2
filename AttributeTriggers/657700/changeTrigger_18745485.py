x=Product.Attr('SC_GN_AT_RB_Service_Products_Saas').GetValue()

Service = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont')


for SP_row in Service.Rows:
    if SP_row['Service_Product'] == x:
        SP_row.IsSelected = True
    else:
        SP_row.IsSelected = False

model_scope=Product.GetContainerByName('SC_GN_AT_Models_Scope_Cont')
invalid_cont=Product.GetContainerByName('SC_GN_AT_Invalid_Cont')

model_scope.Clear()
invalid_cont.Clear()