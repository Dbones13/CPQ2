P =  Product.Attr('SC_Training_Match_Contract_Value_Percent').GetValue()
if P is not None:
    Product.Attr('SC_Training_Match_Contract_Value').Access = AttributeAccess.ReadOnly