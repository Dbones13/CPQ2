Product.Attr('SC_Renewal_check').AssignValue('4')
if Product.Attr('SC_Labor_Service_Product').GetValue() == "A360 Contract Management" and Product.Attr('SC_Labor_Entitlement').GetValue() == "A360 Contract Management" and Product.Attr('SC_Labor_Resource_Type').GetValue() == "A360 Contract Management":
    Product.Attr('SC_Labor_Contigency_Cost').AssignValue('0')