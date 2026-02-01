reference_number=Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal' and reference_number =='':
    Product.Attr("SC_ServiceProduct_HR_RWL").AssignValue(str(Product.Name))
Product.Attr('SC_HWOS_Service_Product').Access = AttributeAccess.ReadOnly