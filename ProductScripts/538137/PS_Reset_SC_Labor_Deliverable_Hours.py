if Product.Attr('SC_Labor_Service_Product').GetValue() == "A360 Contract Management" and Product.Attr('SC_Labor_Entitlement').GetValue() == "A360 Contract Management" and (Product.Attr('SC_Labor_Resource_Type').SelectedValue.ValueCode if Product.Attr('SC_Labor_Resource_Type').SelectedValue != None else '') == "A360 Contract Management" and "A360 Contract Management" not in Product.Attr('SC_ScopeRemoval').GetValue():
    Product.Attr('SC_Labor_Deliverable_Hours').AssignValue('1')
if Product.Attr('SC_Labor_Service_Product').GetValue() == "Service Contract Management" and Product.Attr('SC_Labor_Entitlement').GetValue() == "Service Contract Management" and (Product.Attr('SC_Labor_Resource_Type').SelectedValue.ValueCode if Product.Attr('SC_Labor_Resource_Type').SelectedValue != None else '') == "Service Contract Management" and "Service Contract Management" not in Product.Attr('SC_ScopeRemoval').GetValue():
    Product.Attr('SC_Labor_Deliverable_Hours').AssignValue('1')
if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    SC_ScopeRemoval = eval(Product.Attr('SC_ScopeRemoval').GetValue()) if Product.Attr('SC_ScopeRemoval').GetValue() != '' else []
    SC_Labor_Service_Product = Product.Attr('SC_Labor_Service_Product').GetValue()
    if SC_Labor_Service_Product in SC_ScopeRemoval:
        Product.Attr('SC_Labor_Deliverable_Hours').AssignValue('0')