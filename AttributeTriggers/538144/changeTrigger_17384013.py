Product.Attr('EnabledService_Entitlement').AssignValue(Product.Attr('EnabledServices_servprod').SelectedValue.Display)
####################### if service product is enhanced then order type is required.##################
L3_L4_Mover_Essential_attr = Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel')
Customer_has_cyber_enabledServices = Product.Attr('Customer_has_cyber_enabledServicesModel')
entitlement_value = Product.Attr('EnabledServices_servprod').GetValue()
if Product.Attr('EnabledServices_servprod'):
    if Product.Attr('EnabledServices_servprod').GetValue() == 'Enabled Services - Enhanced':
        Product.Attr('OrderType_EnabledService').Required = True
    else:
        Product.Attr('OrderType_EnabledService').Required = True
#Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue("0.00")
Product_type = Product.Attr('SC_Product_Type').GetValue()
if Product_type == 'Renewal':
    #ScriptExecutor.Execute('GS_SC_ES_Scope_Removal')
    ScriptExecutor.Execute('PS_ES_CompSummary_Validation')
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")
if entitlement_value == 'Enabled Services - Enhanced':
    for i in Customer_has_cyber_enabledServices.Values:
        i.IsSelected = False
    Product.Attr("Customer_has_cyber_enabledServicesModel").Access = AttributeAccess.Editable
    for i in L3_L4_Mover_Essential_attr.Values:
        i.IsSelected = False
    Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable
elif entitlement_value == 'Enabled Services - Essential':
    for i in Customer_has_cyber_enabledServices.Values:
        i.IsSelected = False
    Product.Attr("Customer_has_cyber_enabledServicesModel").Access = AttributeAccess.ReadOnly
    for i in L3_L4_Mover_Essential_attr.Values:
        i.IsSelected = False
    Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable